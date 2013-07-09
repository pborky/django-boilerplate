
__author__ = 'pborky'

import types
from django.contrib import messages
from django.views.decorators import http
from django.http import HttpResponse
from django.conf.urls import url
from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from functional import partial

def autoregister(*app_list):
    for app_name in app_list:
        app_models = get_app(app_name)
        for model in get_models(app_models):
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


class Decorator(object):
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
    def __call__(self, *args, **kwargs):
        return self.func.__call__(*args, **kwargs)

def view(pattern, template = None, form_cls = None, redirect_to = None, redirect_attr = None, invalid_form_msg = 'Form is not valid.', decorators = (), **kwargs):
    class Wrapper(Decorator):
        def __init__(self, obj):
            super(Wrapper, self).__init__(obj)

            if isinstance(obj, types.ClassType):
                obj = obj()

            permitted_methods = {}

            for method in ('get','post', 'option', 'put', 'delete', 'head'):
                if hasattr(obj, method):
                    fnc = getattr(obj, method)
                    if not isinstance(fnc, types.FunctionType):
                        fnc = partial(fnc, obj)
                    permitted_methods[method.upper()] = fnc

                else:
                    # in case we have decorated function instead of class..
                    if hasattr(obj, '__call__'):
                        permitted_methods[method.upper()] = obj
            
            require_http_methods_decorator = http.require_http_methods(request_method_list=permitted_methods.keys())
            for key, val in  permitted_methods.items():
                setattr(self, key.lower(), val)
            
            self.permitted_methods = permitted_methods.keys()
            require_http_methods_decorator = http.require_http_methods(request_method_list=permitted_methods.keys())

            # decorate inner function            
            self.inner = reduce(lambda fnc, dec: dec(fnc), (require_http_methods_decorator,)+decorators, self.inner )
        
        @staticmethod
        def _mk_forms(*args, **kwargs):
            if isinstance(form_cls,tuple) or isinstance(form_cls, list):
                return list(f(*args, **kwargs) for f in form_cls)
            elif isinstance(form_cls, dict):
                return dict((k,f(*args, **kwargs)) for k,f in form_cls.iteritems())
            else:
                if form_cls is not None:
                    return [form_cls(*args, **kwargs),]
                else:
                    return [None,]
        @staticmethod
        def _is_valid(forms):
            if isinstance(forms,dict):
                it = forms.itervalues()
            else:
                it = forms
            return all(f.is_valid() if f is not None else True for f in it)

        def url(self):
            return url(pattern, self, kwargs, self.__name__)

        def __call__(self, *args, **kwargs):
            return self.inner(*args, **kwargs)
            

        def inner(self, request, *args, **kwargs):
            from django.shortcuts import render, redirect
            try:

                if request.method not in self.permitted_methods:
                    return http.HttpResponseNotAllowed(permitted_methods=self.permitted_methods)

                if request.method in ('POST',):

                    forms = self._mk_forms(request.POST)
                    ret =  self.post(request, *args, forms=forms, **kwargs)

                    if isinstance(ret, HttpResponse):
                        return ret

                    if not self._is_valid(forms) and invalid_form_msg:
                        messages.error(request, invalid_form_msg)

                elif request.method in ('GET',) :

                    forms =  self._mk_forms(request.GET) if request.GET else self._mk_forms()

                    ret =  self.get(request, *args, forms=forms, **kwargs)

                    if isinstance(ret, HttpResponse):
                        return ret

                    if not self._is_valid(forms):
                        #forms =  self._mk_forms()
                        #messages.error(request, invalid_form_msg)
                        pass

                elif request.method in ('HEAD', 'OPTION', 'PUT', 'DELETE') :
                    ret =  {}  # not implemented yet
                    forms =  self._mk_forms()

                else:
                    return

            except AttributeError as e:
                raise e
                #return HttpResponseServerError()

            redirect_addr = request.GET[redirect_attr] if redirect_attr in request.GET else redirect_to

            if redirect_addr:
                context_vars = { }

                context_vars.update(kwargs)

                if isinstance(ret,dict):
                    context_vars.update(ret)

                return redirect(redirect_addr, *args, **context_vars)
            else:
                context_vars = {
                            'forms': forms,
                        }
                context_vars.update(kwargs)

                if isinstance(ret,dict):
                    context_vars.update(ret)

                return render(request, template, context_vars)
    return Wrapper





