from pyramid.view import view_config
from pkg_resources import resource_stream
from rdflib import Graph, RDF
from common import *
from common.kg import *
import os.path


class Context:

    def __init__(self, name=None ):
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
        print(index)
        return self


    @property
    def filename(self):
        return self._name

class Syllabus(Context):

    def views(self):
        return {"syll": self.syll}

    @property
    def syll(self):
        self.g.subjects(RDF.type, WPDD['Syllabus'])


class Curriculum(Context):

    def views(self):
        return {"curr": self.curr}

    @property
    def curr(self):
        self.g.subjects(RDF.type, IDD["Curriculum"])

@view_config(route_name='home', renderer='rpd_prep:templates/mytemplate.pt')
def my_view(request):

    syll = request.GET.get("wp", None)
    curr = request.GET.get("cur", None)

    syll = Syllabus(syll)
    curr = Curriculum(curr)

    vars = {}
    for g in [syll, curr]:
        vars.update(g.views())

    return vars


@view_config(route_name='api-1.0', request_method="POST", renderer='json')
def api(request):
    print(request.params)
    error = 0
    status = "ok"
    return {"error": error, "status": status}
