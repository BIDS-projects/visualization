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
    mapper = {}
    graph = Graph.query.filter_by(name=g.map_url).one()
    data = dict()
    import csv
    with open('vis2.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data[row[1]] = row
    vertices = Vertex.query.filter_by(graph_id=graph.id).all()
    print(vertices)
    new_vertices = []
    for i, vertex in enumerate(vertices):
        vertex.i = i
        if vertex.domain not in data:
            print(vertex.domain)
            new_vertices.append({'name':i, 'fullname':'', 
                'link':'#', 'desc':''})
        else:
            print("SUCCESS")
            node = {'name':i, 'fullname':data[vertex.domain][0], 
                'link':data[vertex.domain][1], 'desc':data[vertex.domain][2]}
            new_vertices.append(node)
        mapper[vertex.id] = i
    print(new_vertices[0])
    edges = Edge.query.filter_by(graph_id=graph.id).all()
    most = max(e.weight for e in edges)
    least = min(e.weight for e in edges)
    diff = most - least
    for edge in edges:
        edge.from_v = mapper[edge.from_id]
        edge.to_v = mapper[edge.to_id]
        edge.weight = 5*((edge.weight - least)/diff)
    # temporary randomly-generated categories
    import random
    import json
    categories = dict((c, dict((v.i, random.random()) for v in vertices)) for c in ('Visualization', 'Production', 'Data Science', 'Social Sciences', 'Machine Learning'))
    available = ['0', '169', '190'], ['100', '0', '0'], ['50', '70', '150']
    colors = dict((cat, random.choice(available)) for cat in categories)

    return render_template('topicsmap.html',
        vertices=new_vertices,
        edges=edges,
        categories=categories,
        categories_json=json.dumps(categories),
        colors_json=json.dumps(colors),
        colors=colors)
