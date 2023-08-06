import inspect

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy_types import BaseWithQuery, Column, Timestamp, Validate, types

from ct_core_db.lib import sqla, sqla_types

__version__ = '1.2.0'
__all__ = ['db', 'create_db_session']


########################################
# DB
########################################

db = sqla.SQLAlchemy(metadata=sqla.metadata)


########################################
# DB Model and Mixins
########################################

M = db.Model  # The original Flask-SQAlchemy Model class
Model = declarative_base(cls=(M, BaseWithQuery, sqla.ModelBase, Validate, sqla.HasExternalId))

db.M = M
db.Model = Model
db.Timestamp = Timestamp
db.BaseHas = sqla.BaseHas


########################################
# DB Columns
########################################

def _make_deferred_column(*args, **kwargs):
    return db.deferred(Column(*args, **kwargs))


DeprecatedColumn = _make_deferred_column

db.Column = Column
db.DeprecatedColumn = DeprecatedColumn


########################################
# DB Column Types
########################################

db.JsonUnicodeText = sqla_types.JsonUnicodeText

for k, v in types.__dict__.items():
    if inspect.isclass(v) and issubclass(v, TypeEngine):
        setattr(db, k, v)


########################################
# DB Session
########################################

def create_db_session(app, bind):
    return scoped_session(lambda: create_session(bind=db.get_engine(app, bind)))
