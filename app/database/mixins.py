from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import types as column_types, generic_repr
from datetime import datetime
from app import db
from sqlalchemy.sql import expression
from .softdelete import QueryWithSoftDelete


@generic_repr
class Timestamp(object):
    created = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        nullable=False,)
    updated = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        nullable=False,
                        onupdate=datetime.utcnow)


@generic_repr
class SoftDeleteAttributes(object):
    """
       Use for creating soft deletable models
    """

    @declared_attr
    def active(self):
        return db.Column(db.Boolean,
                         default=True, nullable=False,
                         server_default=expression.true(), index=True)

    query_class = QueryWithSoftDelete


@generic_repr
class StandardAttributes(Timestamp, object):
    """
    Use for creating most models
    """

    @declared_attr
    def id(self):
        return db.Column(db.Integer, primary_key=True, nullable=False)


