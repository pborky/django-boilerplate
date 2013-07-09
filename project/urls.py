from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
import tinymce.urls

from .helpers import autoregister
from .views import login,logout

admin.autodiscover()

autoregister('project')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include(tinymce.urls), name='tinymce'),
)
