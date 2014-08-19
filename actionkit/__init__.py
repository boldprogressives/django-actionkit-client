from actionkit.utils import get_client as Client
import os

"""
ACTIONKIT_API_HOST = os.environ['ACTIONKIT_API_HOST']
ACTIONKIT_API_USER = os.environ['ACTIONKIT_API_USER']
ACTIONKIT_API_PASSWORD = os.environ['ACTIONKIT_API_PASSWORD']

SETTINGS = {
    'ACTIONKIT_API_HOST': ACTIONKIT_API_HOST,
    'ACTIONKIT_API_USER': ACTIONKIT_API_USER,
    'ACTIONKIT_API_PASSWORD': ACTIONKIT_API_PASSWORD,
    }

try:
    import django
except ImportError:
    django = None

if django is not None:
    ACTIONKIT_DATABASE_NAME = os.environ['ACTIONKIT_DATABASE_NAME']
    ACTIONKIT_DATABASE_USER = os.environ['ACTIONKIT_DATABASE_USER']
    ACTIONKIT_DATABASE_PASSWORD = os.environ['ACTIONKIT_DATABASE_PASSWORD']
    
    APIHANGAR_DATABASES = [("ak", "Actionkit")]

    DATABASES = {
        'ak': {
            'ENGINE': "django.db.backends.mysql",
            'NAME': ACTIONKIT_DATABASE_NAME,
            'USER': ACTIONKIT_DATABASE_USER,
            'PASSWORD': ACTIONKIT_DATABASE_PASSWORD,
            'HOST': "client-db.actionkit.com",
            'PORT': "",
            }
        }
    
    CONTEXT_PROCESSORS = [
        'actionkit.context_processors.globals',
        ]


    URLCONFS = [
        (r'', 'actionkit.urls'),
        ]

"""
