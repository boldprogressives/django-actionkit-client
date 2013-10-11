from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'actionkit.views',
    url('^admin/actionkit/test_connection/$',
        'actionkit_test_connection',
        name='actionkit_test_connection'),
    )



