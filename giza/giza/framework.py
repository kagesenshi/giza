from pyramid.interfaces import IViewClassifier, IRequest
from giza.interfaces import IView
from zope.interface import providedBy, implements, Interface, implementedBy
import sys
import os
import venusian
from chameleon import PageTemplateFile

class ViewLookupHelper(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self, name):
        return query_view(self.request, self.context, name)

class View(object):
    implements(IView)

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def render(self):
        return {}

    def __call__(self):
        template = getattr(self, 'template', None)
        if template is not None:
            self.request.response.text = template(
                    context=self.context,
                    request=self.request,
                    view=self,
                    views=ViewLookupHelper(self.context, self.request),
            )

def context(giza_context):
    frame = sys._getframe(1)
    frame.f_locals['giza.context'] = giza_context

def name(giza_name):
    frame = sys._getframe(1)
    frame.f_locals['giza.name'] = giza_name

def template(giza_template):
    frame = sys._getframe(1)
    path = frame.f_globals['__file__']
    template_path = os.path.join(
            os.path.dirname(path), giza_template)
    frame.f_locals['template'] = PageTemplateFile(template_path)

def view(wrapped):
    def callback(context, name, ob):
        config = context.config.with_package(info.module)
        registry = config.registry

        def render(context, request):
            v = ob(context, request)()
            return request.response

        render.__original_view__ = ob

        try:
            giza_context = getattr(ob, 'giza.context')
        except AttributeError:
            raise Exception('Unable to find the context, please use giza.context')

        giza_name = getattr(ob, 'giza.name', '')


        context_iface = giza_context
        if not issubclass(context_iface, Interface):
            context_iface = implementedBy(giza_context)

        registered_views = [a.name for a in (registry.registeredAdapters()
            ) if (IViewClassifier, IRequest, context_iface) == a.required
        ]

        if giza_name in registered_views:
            raise Exception("Conflicting view name '%s'" % giza_name)

        registry.registerAdapter(render, (
            IViewClassifier, IRequest, giza_context), IView, name=giza_name)

    info = venusian.attach(wrapped, callback, category='giza')

    return wrapped


def query_view(request, context, name=''):
    adapters = request.registry.adapters
    obj = adapters.lookup((
        IViewClassifier,
        request.request_iface,
        providedBy(context)), IView, name=name)
    return obj.__original_view__(context, request)
