from pyramid.view import view_config
from pkg_resources import resource_stream
from rdflib import Graph, RDF
from rpd_prep.common import *
from rpd_prep.common.kg import *
import os.path

from chameleon import PageTemplate
import ast


def uppercase_expression(string):

    def compiler(target, engine):
        uppercased = self.string.uppercase()
        value = ast.Str(uppercased)
        return [ast.Assign(targets=[target], value=value)]

    return compiler


PageTemplate.expression_types['rdf'] = uppercase_expression




class Context:

    def __init__(self, name=None):
        self._name = name
        if name is not None:
            self._stream = resource_stream(
                'rpd_prep', os.path.join('..', 'data', name + '.ttl'))
            self.g = Graph()
            binds(self.g)
            self.g.parse(self._stream)

    def views(self):
        """Returns a dictionary of mappings of identifiers to views
        """

        return {}

    def next(self, gen):
        return next(gen)

    def __getitem__(self, index):
        print("INDEX:", index)
        return self

    def _getattr__(self, name):
        print("Attr:", name)
        return self

    @property
    def filename(self):
        return self._name


class Syllabus(Context):

    def views(self):
        return {"syll": self}

    @property
    def syll(self):
        self.g.subjects(RDF.type, WPDD['Syllabus'])


class Curriculum(Context):

    def views(self):
        return {"curr": self}

    @property
    def curr(self):
        self.g.subjects(RDF.type, IDD["Curriculum"])


class View:

    def __init__(self, syll, curr):
        self.syll = syll
        self.curr = curr

    def views(self):
        return {"view": self}


# @view_config(route_name='home', renderer='rpd_prep:templates/mytemplate.pt')
@view_config(route_name='home', renderer='rpd_prep:templates/mytemplate.pt')
def my_view(request):

    syll = request.GET.get("wp", None)
    curr = request.GET.get("cur", None)

    syll = Syllabus(syll)
    curr = Curriculum(curr)
    view = View(syll, curr)

    vars = {}
    for g in [syll, curr, view]:
        vars.update(g.views())

    return vars


@view_config(route_name='api-1.0', request_method="POST", renderer='json')
def api(request):
    print(request.params)
    error = 0
    status = "ok"
    return {"error": error, "status": status}


# @subscriber(BeforeRender)
# def correct_experssion_types(event):
#     renderer_info = event["renderer_info"]
#     render_factory_pt = renderer_info.registry.queryUtility(IRendererFactory, '.pt')
#     render_factory_txt = renderer_info.registry.queryUtility(IRendererFactory, '.txt')
#     print("RF:", render_factory_pt, render_factory_txt)
