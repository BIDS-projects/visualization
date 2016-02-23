from flask import Blueprint, g, render_template
from visualization.models import Graph, Vertex, Edge

maps = Blueprint('maps', __name__, url_prefix='/<string:map_url>')


######################
# DEFAULT PROCESSORS #
######################


@maps.url_defaults
def add_map_url(endpoint, values):
    values.setdefault('map_url', getattr(g, 'map_url', None))


@maps.url_value_preprocessor
def pull_map_url(endpoint, values):
    g.map_url = values.pop('map_url')


#########
# VIEWS #
#########

@maps.route('/')
def home():
    graph = Graph.query.filter_by(name=g.map_url).one()
    return render_template('topicsmap.html',
        vertices=Vertex.query.filter_by(graph_id=graph.id).all(),
        edges=Vertex.query.filter_by(graph_id=graph.id).all())
