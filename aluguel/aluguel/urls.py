from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('imoveis.urls', namespace='imoveis')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
