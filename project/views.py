__author__ = 'pborky'

from django.contrib import messages
from django.views.decorators import cache, http
from django.contrib.auth.decorators import login_required

from .helpers import view
from .forms import LoginForm


@view(
    r'^login/do$',
    form_cls = {'login':LoginForm,},
    invalid_form_msg = 'Login form invalid.',
    redirect_to = '/',
    redirect_attr = 'next',
    decorators = ( cache.never_cache,  ),
)
class do_login:
    @staticmethod
    def post(request, forms):
        from django.contrib.auth import login,authenticate
        form = forms['login']
        try:
            if form.is_valid():
                user = authenticate(username=form.data.get('username'), password=form.data.get('password'))
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'User authentication was successful.')
                        return
                    else:
                        messages.error(request, 'User account has been disabled.')
                        return
        except Exception:
            pass
        messages.error(request, 'User authentication was unsuccessful.')


@view(
    r'^login$',
    template = 'login.html',
    decorators = ( cache.never_cache,  ),
)
class login:
    @staticmethod
    def get(request, forms):
        return {
            'next': request.GET['next'] if 'next' in request.GET else request.POST['next'] if 'next' in request.POST else '/'
        }

@view(
    r'^logout$',
    redirect_to = '/',
    redirect_attr = 'next',
    decorators = ( cache.never_cache,  ),
)
class logout:
    @staticmethod
    def get(request, forms):
        from django.contrib.auth import logout
        logout(request)
        messages.success(request, 'User deauthentication successful.')
