from pyramid.view import view_config
from giza.models import MyModel
from giza.resources import giza_resources

@view_config(context=MyModel, renderer='templates/mytemplate.pt')
def my_view(request):
    giza_resources.need()
    return {'project':'giza'}
