from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

# Flask app
app = Flask(__name__)

# Set configuration
config = DevelopmentConfig

# Configuration for mySQL database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
#     username=config.username,
#     password=config.password,
#     host=config.host,
#     database=config.database
# )
# db = SQLAlchemy(app)

from visualization.maps.views import maps
from visualization.public.views import public

for blueprint in (maps, public):
    app.register_blueprint(blueprint)
