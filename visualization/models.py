"""
Database Models
---
BIDS Institutional Ecosystem Mapping

This is the standard structure for all BIDS IEM data. All maps will at
minimum contain information about the following.
"""

import sqlalchemy.ext.declarative as sad
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy_utils import ArrowType
import arrow


class Base(sad.declarative_base(), object):
    """MySQL base object"""

    __abstract__ = True
    db = None

    id = Column(Integer, primary_key=True)
    updated_at = Column(ArrowType)
    updated_by = Column(Integer)
    created_at = Column(ArrowType, default=arrow.now('US/Pacific'))
    created_by = Column(Integer)
    is_active = Column(Boolean, default=True)

    @classmethod
    def get_or_create(cls, **data):
        """Get or create the object"""
        return cls.query().filter_by(**data).one_or_none() or cls(**data).save()

    def update(self, **kwargs):
        """updates object with kwargs"""
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    @classmethod
    def query(cls):
        """Returns query object"""
        return cls.db.session.query(cls)

    def add(self):
        """save object to database"""
        self.db.session.add(self)
        return self

    def save(self):
        """save object to database"""
        self.db.session.add(self)
        self.db.session.commit()
        return self


ForeignColumn = lambda *args, **kwargs: sad.declared_attr(
    lambda _: Column(*args, **kwargs))


##########
# MODELS #
##########


class Graph(Base):
    """abstract for a graph"""

    __tablename__ = 'graph'

    name = Column(Text)
    directed = Column(Boolean)
    vertices = relationship('Vertex', backref='graph')
    edges = relationship('Edge', backref='graph')


class Vertex(Base):
    """abstract for a graph vertex"""

    __abstract__ = True

    name = Column(String(50), unique=True)
    value = Column(Text)
    graph_id = ForeignColumn(Integer, ForeignKey('graph.id'))


class Edge(Base):
    """abstract for a graph edge"""

    __abstract__ = True

    value = Column(Integer)

    graph_id = ForeignColumn(Integer, ForeignKey('graph.id'))
    from_id = Column(Integer)
    from_domain = Column(BLOB())
    to_id = Column(Integer)
    to_domain = Column(BLOB())