from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
import tinymce.urls

from .helpers import autoregister
from .views import login,logout,login,do_login

admin.autodiscover()

autoregister('project')

urlpatterns = patterns('',
    do_login.url(),
    login.url(),
    logout.url(),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include(tinymce.urls), name='tinymce'),
)
