from forms import LoginForm

__author__ = 'pborky'

from models import SiteResource

def site_data(request):
    return {
        'site_resource': dict((s.name, s.value) for s in SiteResource.objects.all()),
        }

def login_form(request):
    return {
        'login_form': LoginForm()
    }