from fanstatic import Library
from fanstatic import Resource
from fanstatic import Group
#from js.lesscss import LessResource
from js.bootstrap import bootstrap_responsive_css, bootstrap
from js.jquery import jquery
from js.jquery_tools import jquery_tools

library = Library('giza', 'resources')

gridster_js = Resource(library, 'gridster/jquery.gridster.js',
        depends=[jquery])

gridster_css = Resource(library, 'gridster/jquery.gridster.css')


css_resource = Resource(library, 'main.css', depends=[bootstrap_responsive_css])

js_resource = Resource(library, 'main.js', bottom=True, depends=[bootstrap,
    gridster_js])


#less_resource = LessResource(library, 'main.less')

giza_resources = Group([gridster_css, jquery_tools,
                        css_resource, js_resource,
#                     less_resource,
                    ])


def pserve():
    """A script aware of static resource"""
    import pyramid.scripts.pserve
    import pyramid_fanstatic
    import os

    dirname = os.path.dirname(__file__)
    dirname = os.path.join(dirname, 'resources')
    pyramid.scripts.pserve.add_file_callback(
                pyramid_fanstatic.file_callback(dirname))
    pyramid.scripts.pserve.main()
