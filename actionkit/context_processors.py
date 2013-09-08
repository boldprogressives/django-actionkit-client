from django.conf import settings

def globals(request):
    return {
        'ACTIONKIT_URL': settings.ACTIONKIT_API_HOST,
        }
