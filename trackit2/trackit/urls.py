"""trackit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
handler404 = 'expans.views.handler_404'
handler500 = 'expans.views.custom_error_view'
handler403 = 'expans.views.custom_permission_denied_view'
handler400 = 'expans.views.custom_bad_request_view'

urlpatterns = patterns('',
    url(r'^expans/', include('expans.urls')),
    # url(r'^http://localhost:8000/expans/', 'expans.views.index'),
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
)



if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),)