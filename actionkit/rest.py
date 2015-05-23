from actionkit.models import QueryReport
from django.conf import settings
import json
import requests
from requests.auth import HTTPBasicAuth

TIMEOUT = getattr(settings, 'ACTIONKIT_API_TIMEOUT', None)

def request(url, method, **kw):
    if 'timeout' not in kw and TIMEOUT is not None:
        kw['timeout'] = TIMEOUT
    return getattr(requests, method)(
        url, allow_redirects=False, 
        auth=(settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
        **kw)

class client(object):
    def __init__(self, safety_net=True):
        self.safety_net = safety_net

    @property
    def base_url(self):
        host = settings.ACTIONKIT_API_HOST
        if not host.startswith("https"):
            host = "https://" + host
        url = "%s/rest/v1/" % host
        return url

    def dir(self):
        resp = request(self.base_url, "get")
        assert resp.status_code == 200, resp.text
        return resp.json.keys()

    def __getattr__(self, attr):
        if not self.safety_net:
            return ClientResourceHandler(attr, object_methods=["get", "put", "delete", "patch"],
                                         collection_methods=["get", "post"])
            
        url = self.base_url + attr + "/schema/"
        resp = request(url, "get")
                            
        if resp.status_code == 404:
            raise AttributeError("No known resource %s" % attr)
        assert resp.status_code == 200, resp.text
        try:
            methods = resp.json()['allowed_detail_http_methods']
        except TypeError:
            raise AttributeError("No known resource %s" % attr)
        collection_methods = resp.json()['allowed_list_http_methods']
        return ClientResourceHandler(attr, object_methods=methods,
                                     collection_methods=collection_methods)

class ResourceDoesNotExist(Exception):
    pass

class ClientResourceHandler(object):
    def __init__(self, resource, object_methods=[], collection_methods=[]):
        self.resource = resource
        self.object_methods = object_methods
        self.collection_methods = collection_methods

    def __repr__(self):
        return "<ResourceHandler %s %s>" % (self.resource, 
                                            repr(self.object_methods))
    
    @property
    def base_url(self):
        host = settings.ACTIONKIT_API_HOST
        if not host.startswith("https"):
            host = "https://" + host
        url = "%s/rest/v1/%s/" % (host, self.resource)
        return url

    def check_collection_method(self, method):
        if method not in self.collection_methods:
            raise NotImplementedError("Cannot %s collection %s" % (method, self.resource))

    def check_method(self, method):
        if method not in self.object_methods:
            raise NotImplementedError("Cannot %s objects of type %s" % (method, self.resource))

    def _get(self, id):
        self.check_method("get")
        resp = request(self.base_url + "%s/" % id, "get")
        if resp.status_code == 404:
            return None
        assert resp.status_code == 200, resp
        return resp.json()

    def get(self, id):
        obj = self._get(id)
        if obj is None:
            raise ResourceDoesNotExist(id)
        return obj

    def exists(self, id):
        return self._get(id)

    def patch(self, id, **kw):
        self.check_method("patch")
        resp = request(self.base_url + "%s/" % id, "patch", 
                       headers={'content-type': 'application/json'},
                       data=json.dumps(kw))
        assert resp.status_code == 202, (resp, resp.text)
    
    def put(self, id, **kw):
        self.check_method("put")
        resp = request(self.base_url + "%s/" % id, "put", 
                       headers={'content-type': 'application/json'},
                       data=json.dumps(kw))
        assert resp.status_code == 204, (resp, resp.text)
        
    def delete(self, id):
        self.check_method("delete")
        resp = request(self.base_url + "%s/" % id, "delete")        
        assert resp.status_code == 204, (resp, resp.text)
        
    def list(self):
        self.check_collection_method("get")

    def create(self, **kw):
        self.check_collection_method("post")
        resp = request(self.base_url, "post", 
                       headers={'content-type': 'application/json'},
                       data=json.dumps(kw))
        assert resp.status_code == 201, (resp, resp.text)
        location = resp.headers['Location']
        assert location.startswith(self.base_url), "Unexpected location %s" % location
        id = location[len(self.base_url):]
        id = id.strip("/")
        return id

def run_query(sql):
    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host
    
    url = "%s/rest/v1/report/run/sql/" % host
    resp = requests.post(url, auth=HTTPBasicAuth(
            settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
                         headers={'content-type': 'application/json',
                                  'accept': 'application/json'},
                         data=json.dumps({'query': sql}),
                         timeout=TIMEOUT)
    assert resp.status_code == 200, resp.text
    return resp.json()

def create_report(sql, description, name, short_name):
    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host

    data = json.dumps(dict(sql=sql, description=description, 
                           name=name, short_name=short_name,
                           hidden=True, 
                           #refresh=True, full_recalc=True,
                           ))

    url = "%s/rest/v1/queryreport/" % host
    resp = requests.post(url, auth=HTTPBasicAuth(
            settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
                         headers={'content-type': 'application/json'},
                         data=data,
                         timeout=TIMEOUT)
    assert resp.status_code == 201, resp.text
    location = resp.headers['Location']
    return {"id": location.strip("/").split("/")[-1], "short_name": short_name}

def unhide_report(report_id):
    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host

    report = QueryReport.objects.using("ak").select_related("report_ptr").get(
        report_ptr__id=report_id)
    data = json.dumps(dict(hidden=False, 
                           sql=report.sql, name=report.report_ptr.name,
                           short_name=report.report_ptr.short_name))
    url = "%s/rest/v1/queryreport/%s/" % (host, report_id)

    resp = requests.put(url, auth=HTTPBasicAuth(
            settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
                        headers={'content-type': 'application/json'},
                        data=data,
                        timeout=TIMEOUT)
    assert resp.status_code == 201

def delete_report(report_id):
    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host

    url = "%s/rest/v1/queryreport/%s/" % (host, report_id)
    resp = requests.delete(url, auth=HTTPBasicAuth(
            settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
                           timeout=TIMEOUT)
    assert resp.status_code == 204

def run_report(name, email_to=None, data=None):
    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host

    data = data or {}
    data['refresh'] = True
    data['full_recalc'] = True
    
    if email_to is not None:
        data['use_email'] = True
        data['email'] = email_to
    
    url = "%s/rest/v1/report/background/%s/" % (host, name)
    resp = requests.post(url, auth=HTTPBasicAuth(
            settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
                         data=data,
                         headers={'Accept': "text/csv"},
                         timeout=TIMEOUT)

    assert resp.status_code == 201
    location = resp.headers['Location']
    return location.strip("/").split("/")[-1]

def poll_report(akid):

    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host

    url = "%s/rest/v1/backgroundtask/%s/" % (host, akid)
    resp = requests.get(url, auth=HTTPBasicAuth(
            settings.ACTIONKIT_API_USER, settings.ACTIONKIT_API_PASSWORD),
                        headers={'content-type': 'application/json'},
                        timeout=TIMEOUT)

    assert resp.status_code == 200
    results = json.loads(resp.content)

    return results

