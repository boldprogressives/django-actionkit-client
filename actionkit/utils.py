from django.conf import settings
from urlparse import urlparse
import xmlrpclib

def get_client():
    host = settings.ACTIONKIT_API_HOST
    if not host.startswith("https"):
        host = "https://" + host
    host = urlparse(host)
    url = '%s://%s:%s@%s/api/' % (
            host.scheme,
            settings.ACTIONKIT_API_USER,
            settings.ACTIONKIT_API_PASSWORD,
            host.netloc)
    actionkit = xmlrpclib.Server(url)
    return actionkit
