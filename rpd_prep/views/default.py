from pyramid.view import view_config
from pkg_resources import resource_stream
from rdflib import Graph, RDF
from rpd_prep.common import WPDD
import os.path


class Context:

    def __init__(self, name):
        self._name = name
        if name is not None:
            self._stream = resource_stream(
                'rpd_prep', os.path.join('..', 'data', name + '.ttl'))
            self.g = Graph()
            self.g.parse(self._stream)

    @property
    def syll(self):
        return self.g.subjects(RDF.type, WPDD['Syllabus'])


@view_config(route_name='home', renderer='rpd_prep:templates/mytemplate.pt')
def my_view(request):
    name = request.GET.get("wp", None)
    context = Context(name)
    if name:
        context.about = name

    return {'project': 'rpd-prep', "context": context}


@view_config(route_name='api-1.0', request_method="POST", renderer='json')
def api(request):
    print(request.params)
    error = 0
    status = "ok"
    return {"error": error, "status": status}
