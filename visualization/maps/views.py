from flask import Blueprint, g, render_template


maps = Blueprint('maps', __name__, url_prefix='/<string:map_url>')


######################
# DEFAULT PROCESSORS #
######################


@maps.url_defaults
def add_map_url(endpoint, values):
    values.setdefault('map_url', getattr(g, 'queue_url', None))


@maps.url_value_preprocessor
def pull_map_url(endpoint, values):
    g.map_url = values.pop('map_url')


#########
# VIEWS #
#########

@maps.route('/')
def home():
    return render_template('map.html')
