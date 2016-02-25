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
    new_vertices = []
    for i, vertex in enumerate(vertices):
        vertex.i = i
        if vertex.domain not in data:
            new_vertices.append({'name':i, 'fullname':'', 
                'link':'berkeley.edu', 'desc':''})
        else:
            node = {'name':i, 'fullname':data[vertex.domain][0], 
                'link':data[vertex.domain][1], 'desc':data[vertex.domain][2]}
            new_vertices.append(node)
        mapper[vertex.id] = i
    edges = Edge.query.filter_by(graph_id=graph.id).all()
    mean = sum(e.weight for e in edges)/len(edges)
    sigma = (sum((e.weight-mean)**2 for e in edges)/len(edges))**.5
    edges = [edge for edge in edges if edge.weight > mean+sigma]
    mean = sum(e.weight for e in edges)/len(edges)
    sigma = (sum((e.weight-mean)**2 for e in edges)/len(edges))**.5
    most = max(e.weight for e in edges)
    least = min(e.weight for e in edges)
    diff = most - least
    for edge in edges:
        edge.from_v = mapper[edge.from_id]
        edge.to_v = mapper[edge.to_id]
        edge.weight = 3 + (edge.weight-mean)/sigma
        #edge.weight = 5*((edge.weight - least)/diff)
    # temporary randomly-generated categories
    import random
    import json
    categories = dict((c, dict((v['fullname'], random.random()) for v in new_vertices)) for c in ('Visualization', 'Production', 'Data Science', 'Social Sciences', 'Machine Learning'))
    available = ['159', '178', '79'],['70', '116', '178'], ['255', '131', '116'],['125', '181', '255'], ['179', '204', '80'],['205','220','57'],['255','193','7'],['67', '117', '178'],['255', '121', '108']
    colors = dict(((cat, color) for color,cat in zip(random.sample(available,len(categories)),categories)))

    return render_template('topicsmap.html',
        vertices=new_vertices,
        edges=edges,
        categories=categories,
        categories_json=json.dumps(categories),
        colors_json=json.dumps(colors),
        colors=colors)
