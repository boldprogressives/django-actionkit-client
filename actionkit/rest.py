try:
    from actionkit.models import QueryReport
    from django.conf import settings
except ImportError:
    import os
    QueryReport = None
    NULL = object()
    class Settings(object):
        def __getattr__(self, attr, default=NULL):
            try:
                return os.environ[attr]
            except KeyError:
                if default is NULL:
                    raise AttributeError
                else:
                    return default
    settings = Settings()

import json
import requests
from requests.auth import HTTPBasicAuth
from csv import DictReader

TIMEOUT = getattr(settings, 'ACTIONKIT_API_TIMEOUT', None)

def request(url, method, **kw):
    if 'timeout' not in kw and TIMEOUT is not None:
        kw['timeout'] = TIMEOUT

    api_user = kw.pop('api_user', settings.ACTIONKIT_API_USER)
    api_password = kw.pop('api_password', settings.ACTIONKIT_API_PASSWORD)
        
    return getattr(requests, method)(
        url, allow_redirects=False, 
        auth=(api_user, api_password),
        **kw)

class client(object):
    def __init__(
            self,
            safety_net=False,
            api_host=None,
            api_user=None,
            api_password=None
    ):
        self.safety_net = safety_net
        self.api_host = api_host or settings.ACTIONKIT_API_HOST
        self.api_user = api_user or settings.ACTIONKIT_API_USER
        self.api_password = api_password or settings.ACTIONKIT_API_PASSWORD
        
    @property
    def base_url(self):
        host = self.api_host
        if not host.startswith("https"):
            host = "https://" + host
        url = "%s/rest/v1/" % host
        return url

    def dir(self):
        resp = request(self.base_url, "get", api_user=self.api_user, api_password=self.api_password)
        assert resp.status_code == 200, resp.text
        return resp.json.keys()

    def __getattr__(self, attr):
        if not self.safety_net:
            return ClientResourceHandler(attr, object_methods=["get", "put", "delete", "patch"],
                                         collection_methods=["get", "post"], 
                                         api_user=self.api_user, api_password=self.api_password, api_host=self.api_host)
            
        url = self.base_url + attr + "/schema/"
        resp = request(url, "get", api_user=self.api_user, api_password=self.api_password)
                            
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
    def __init__(self, resource, object_methods=[], collection_methods=[],
                 api_host=None,
                 api_user=None,
                 api_password=None):
        self.resource = resource
        self.object_methods = object_methods
        self.collection_methods = collection_methods
        self.api_host = api_host or settings.ACTIONKIT_API_HOST
        self.api_user = api_user or settings.ACTIONKIT_API_USER
        self.api_password = api_password or settings.ACTIONKIT_API_PASSWORD

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
        resp = request(self.base_url + "%s/" % id, "get", api_user=self.api_user, api_password=self.api_password)
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
                       api_user=self.api_user, api_password=self.api_password,
                       headers={'content-type': 'application/json'},
                       data=json.dumps(kw))
        assert resp.status_code == 202, (resp, resp.text)
    
    def put(self, id, **kw):
        self.check_method("put")
        resp = request(self.base_url + "%s/" % id, "put", api_user=self.api_user, api_password=self.api_password, 
                       headers={'content-type': 'application/json'},
                       data=json.dumps(kw))
        assert resp.status_code == 204, (resp, resp.text)
        
    def delete(self, id):
        self.check_method("delete")
        resp = request(self.base_url + "%s/" % id, "delete", api_user=self.api_user, api_password=self.api_password)        
        assert resp.status_code == 204, (resp, resp.text)
        
    def list(self, **kw):
        self.check_collection_method("get")
        resp = request(self.base_url, "get", params=kw, api_user=self.api_user, api_password=self.api_password)        
        assert resp.status_code == 200, (resp, resp.text)        
        return resp.json()

    def create(self, **kw):
        self.check_collection_method("post")
        resp = request(self.base_url, "post", api_user=self.api_user, api_password=self.api_password, 
                       headers={'content-type': 'application/json'},
                       data=json.dumps(kw))
        assert resp.status_code == 201, (resp, resp.text)
        location = resp.headers['Location']
        if '/action/' not in self.base_url and '/eraser/' not in self.base_url:
            assert location.startswith(self.base_url), "Unexpected location %s" % location
            id = location[len(self.base_url):]
        else:
            id = location.strip("/").split("/")[-1]
        return id

def run_query(sql, api_host=None, api_user=None, api_password=None, format=None):
    host = api_host or settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host
    
    url = "%s/rest/v1/report/run/sql/" % host

    data = json.dumps({'query': sql, 'refresh': True, 'cache_duration': 1})
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}
    if format and 'csv' in format:
        headers['accept'] = 'text/csv'
        
    resp = requests.post(
        url, auth=HTTPBasicAuth(
            api_user or settings.ACTIONKIT_API_USER,
            api_password or settings.ACTIONKIT_API_PASSWORD
        ),
        headers=headers,
        data=data,
        timeout=TIMEOUT
    )
    assert resp.status_code == 200, resp.text

    if format and 'csv' in format:
        return DictReader(resp.iter_lines(decode_unicode=True))
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

    if QueryReport is None:
        raise RuntimeError("this function requires Django for some reason.")
    
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

