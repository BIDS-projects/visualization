"""
Database Models
---
BIDS Institutional Ecosystem Mapping

This is the standard structure for all BIDS IEM data. All maps will at
minimum contain information about the following.
"""

from visualization import db
import sqlalchemy.ext.declarative as sad
from sqlalchemy_utils import ArrowType
import arrow


class Base(db.Model):
    """MySQL base object"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(ArrowType)
    updated_by = db.Column(db.Integer)
    created_at = db.Column(ArrowType, default=arrow.now('US/Pacific'))
    created_by = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

    @classmethod
    def get_or_create(cls, **data):
        """Get or create the object"""
        return cls.query.filter_by(**data).one_or_none() or cls(**data).save()

    def update(self, **kwargs):
        """updates object with kwargs"""
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def add(self):
        """save object to database"""
        db.session.add(self)
        return self

    def save(self):
        """save object to database"""
        db.session.add(self)
        db.session.commit()
        return self


ForeignColumn = lambda *args, **kwargs: sad.declared_attr(
    lambda _: db.Column(*args, **kwargs))


#############
# CONTRACTS #
#############


class Graph(Base):
    """abstract for a graph"""

    __tablename__ = 'graph'

    name = db.Column(db.Text)
    directed = db.Column(db.Boolean)
    vertices = db.relationship('Vertex', backref='graph')
    edges = db.relationship('Edge', backref='graph')


class Vertex(Base):
    """abstract for a graph vertex"""

    __abstract__ = True

    name = db.Column(db.String(50), unique=True)
    value = db.Column(db.Text)
    graph_id = ForeignColumn(db.Integer, db.ForeignKey('graph.id'))

class Edge(Base):
    """abstract for a graph edge"""

    __abstract__ = True

    value = db.Column(db.String(50))

    graph_id = ForeignColumn(db.Integer, db.ForeignKey('graph.id'))
    from_id = ForeignColumn(db.Integer, db.ForeignKey('vertex.id'))
    to_id = ForeignColumn(db.Integer, db.ForeignKey('vertex.id'))


##########
# MODELS #
##########

V = Vertex
E = Edge

class Edge(E):
    """lda edge abstract"""

    __tablename__ = 'edge'

    weight = db.Column(db.Integer)


class Vertex(V):
    """lda vertex abstract"""

    __tablename__ = 'vertex'

    domain = db.Column(db.Text)


class TopicVertex(Base):

    __tablename__ = 'topic_vertex'

    topic_id = ForeignColumn(db.Integer, db.ForeignKey('topic.id'))
    vertex_id = ForeignColumn(db.Integer, db.ForeignKey('vertex.id'))


class Keyword(Base):

    __tablename__ = 'keyword'

    name = db.Column(db.String(50), unique=True)


class KeywordTopic(Base):

    __tablename__ = 'keyword_topic'
    topic_id = ForeignColumn(db.Integer, db.ForeignKey('topic.id'))
    keyword_id = ForeignColumn(db.Integer, db.ForeignKey('keyword.id'))


class Topic(Base):

    __tablename__ = 'topic'

    name = db.Column(db.String(50), unique=True)
