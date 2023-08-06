from flask.signals import Namespace
from flask_sqlalchemy import (
    Model as BaseModel,
    SignallingSession as BaseSignallingSession,
    SQLAlchemy as BaseSQLAlchemy)
from sqlalchemy import MetaData, event, inspect
from sqlalchemy.orm.session import object_session


########################################
# SQLAlchemy
########################################

# Signalling session enhancements
_signals = Namespace()
models_committed = _signals.signal('models-committed')
before_models_committed = _signals.signal('before-models-committed')


class SQLAlchemy(BaseSQLAlchemy):
    def create_session(self, options):
        return SignallingSession(self, **options)


class SignallingSession(BaseSignallingSession):
    def __init__(self, *args, **kwargs):
        super(SignallingSession, self).__init__(*args, **kwargs)
        _SessionSignalEvents.register(self)


class _SessionSignalEvents(object):
    """Uses a better version of modification tracking that avoids PK collisions.

    Copied from Flask-SQLAlchemy at fe67c633f2e6d66a01a1670e5fc6649506358d20
    """
    @classmethod
    def register(cls, session):
        if not hasattr(session, '_fixed_model_changes'):
            session._fixed_model_changes = {}

        event.listen(session, 'before_flush', cls.record_ops)
        event.listen(session, 'before_commit', cls.record_ops)
        event.listen(session, 'before_commit', cls.before_commit)
        event.listen(session, 'after_commit', cls.after_commit)
        event.listen(session, 'after_rollback', cls.after_rollback)

    @classmethod
    def unregister(cls, session):
        if hasattr(session, '_fixed_model_changes'):
            del session._fixed_model_changes

        event.remove(session, 'before_flush', cls.record_ops)
        event.remove(session, 'before_commit', cls.record_ops)
        event.remove(session, 'before_commit', cls.before_commit)
        event.remove(session, 'after_commit', cls.after_commit)
        event.remove(session, 'after_rollback', cls.after_rollback)

    @staticmethod
    def record_ops(session, flush_context=None, instances=None):
        try:
            d = session._fixed_model_changes
        except AttributeError:
            return

        for targets, operation in ((session.new, 'insert'), (session.dirty, 'update'), (session.deleted, 'delete')):
            for target in targets:
                state = inspect(target)
                key = state.identity_key if state.has_identity else id(target)
                d[key] = (target, operation)

    @staticmethod
    def before_commit(session):
        try:
            d = session._fixed_model_changes
        except AttributeError:
            return

        if d:
            before_models_committed.send(session.app, changes=list(d.values()))

    @staticmethod
    def after_commit(session):
        try:
            d = session._fixed_model_changes
        except AttributeError:
            return

        if d:
            models_committed.send(session.app, changes=list(d.values()))
            d.clear()

    @staticmethod
    def after_rollback(session):
        try:
            d = session._fixed_model_changes
        except AttributeError:
            return

        d.clear()


########################################
# MetaData
########################################

_naming_convention = {
    'ix': "ix_%(column_0_label)s",
    'uq': "uq_%(table_name)s_%(column_0_name)s",
    'ck': "ck_%(table_name)s_%(constraint_name)s",
    'fk': "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    'pk': "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=_naming_convention)


########################################
# ModelBase
########################################

class ModelBase(object):
    @classmethod
    def __find_base_class(cls, search):
        bases = search.__bases__
        if BaseModel in bases:
            return search
        else:
            for base in bases:
                r = cls.__find_base_class(base)
                if r:
                    return r
        return None

    @classmethod
    def entity_type(cls, use_base=True):
        if use_base:
            return unicode(cls.__find_base_class(cls).__name__)
        return unicode(cls.__name__)

    @classmethod
    def get_tablename(cls):
        return cls.__find_base_class(cls).__tablename__

    def to_tuple(self, use_base=True):
        return self.entity_type(use_base=use_base), self.id

    def update(self, values):
        for key, value in values.items():
            if hasattr(self, key) and key not in ('id', ):
                setattr(self, key, value)

    def _can_cast(self, cls):
        """
        allow the developer to override what class can be cast to what
        """
        return issubclass(self.__class__, cls) or issubclass(cls, self.__class__)

    def cast(self, cls):
        Session = object_session(self)

        if self in Session.dirty:
            raise Exception('Please flush object before casting.')

        if cls.__mapper__.polymorphic_identity:
            if self._can_cast(cls):
                Session.execute('update `{}` set row_type="{}" where id={}'.format(
                    cls.__tablename__, cls.__mapper__.polymorphic_identity, self.id))
                Session.expunge(self)
                return cls.for_id(self.id)
            else:
                raise Exception('Not allow to cast {} to {}'.format(self, cls))
        else:
            raise Exception('Unable to find row_type, this may not be a polymorphic object: {}'.format(self,))

    def duplicate(self):
        session = object_session(self)

        if self in session.dirty:
            raise Exception('Please flush object before copying.')

        arguments = dict()
        for name, column in self.__mapper__.columns.items():
            if not (column.primary_key or column.unique):
                arguments[name] = getattr(self, name)
        return self.__class__(**arguments)

    def __repr__(self):
        try:
            # Use __dict__ to be absolutely sure we won't issue any SQL by accessing id.
            id_ = self.__dict__.get('id', None)
            if id_ is not None:
                klass = type(self)
                return '<{} {}>'.format(klass.__name__, id_)
            else:
                return super(ModelBase, self).__repr__()
        except Exception:
            return super(ModelBase, self).__repr__()


########################################
# BaseHas
########################################

class BaseHas(object):
    __mapping__ = {}

    @classmethod
    def __find_direct_descendant(cls, search, parent):
        bases = search.__bases__
        if BaseHas in bases:
            return parent
        else:
            for base in bases:
                r = cls.__find_direct_descendant(base, search)
                if r:
                    return r
        return None

    @classmethod
    def discriminator(cls):
        # need this so that subclassing doesn't create
        # another discriminator/namespace
        if not hasattr(cls, 'base_class'):
            cls.base_class = cls.__find_direct_descendant(cls, cls)
        return cls.base_class.__name__.lower()

    @classmethod
    def register(cls, key, creator):
        full_key = '{}_{}'.format(cls.discriminator(), key)
        cls.__mapping__[full_key] = creator

    def __getattribute__(self, key):
        value = object.__getattribute__(self, key)
        if key.startswith('__'):
            return value

        full_key = '{}_{}'.format(object.__getattribute__(self, '__class__').discriminator(), key)
        if value is None and full_key in self.__mapping__:
            value = self.__mapping__[full_key]([])
            setattr(self, key, value)
        return value


########################################
# HasExternalId
########################################

class HasExternalId(object):
    @staticmethod
    def __temp_to_internal_func(_):
        raise NotImplementedError(
            'Set `_to_internal_func` to a function that converts an external identifier to an internal one.')

    @staticmethod
    def __temp_to_external_func(_):
        raise NotImplementedError(
            'Set `_to_external_func` to a function that converts an internal identifier to an external one.')

    _to_internal_func = __temp_to_internal_func
    _to_external_func = __temp_to_external_func

    @classmethod
    def for_external_id(cls, external_id):
        try:
            id_ = cls._to_internal_func(external_id)
        except ValueError:
            return None
        return cls.query.filter_by(id=id_).first()

    @property
    def external_id(self):
        return self._to_external_func(self.id)
