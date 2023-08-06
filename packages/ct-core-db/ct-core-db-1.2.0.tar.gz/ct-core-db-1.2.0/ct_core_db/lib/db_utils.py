import re
from contextlib import contextmanager
from pprint import pprint

from flask_sqlalchemy import get_debug_queries, connection_stack
from sqlalchemy import event, inspect

from ct_core_db import db, sqla

WHITESPACE_RE = re.compile(ur'\s+', re.U)
SELECT_CLAUSE_RE = re.compile(ur'SELECT(.*?)FROM\s', re.M | re.S | re.I | re.U)


########################################
# Obfuscation Helpers
########################################

def _obfuscate_string_col(string_field):
    """SQL function that creates a repeated MD5 hash of a string column that has the same length as the original.
    :param string_field: An `InstrumentedAttribute` for a string-based `Column`.
    :return: SQLAlchemy function
    """
    return db.func.trim(
        db.func.left(
            db.func.repeat(
                db.func.md5(string_field),
                db.func.floor(db.func.char_length(string_field) / 32) + 1),
            db.func.char_length(string_field)))


def obfuscate_model_data(db_session, model, *excluded_column_keys):
    """Obfuscate all data for this model, excluding columns whose key is among `excluded_column_keys`."""
    print('\n'.join(['*' * 80, "Obfuscating model: {} ({})...".format(model.__name__, model.__table__.name)]))
    if excluded_column_keys:
        print("Excluding columns: {}".format(excluded_column_keys))

    for col in model.__table__.c:
        ia = inspect(col)
        if ia.key not in excluded_column_keys:
            obfuscate_func = None
            if isinstance(ia.type, (db.Email, db.String, db.Unicode, db.UnicodeText)):
                obfuscate_func = _obfuscate_string_col

            if obfuscate_func:
                print("Obfuscating column: {} ({})...".format(ia.key, ia.name))
                # Bulk update all rows for this column that are not null
                stmt = ia.table.update().where(col.isnot(None)).values({ia.name: obfuscate_func(col)})
                db_session.execute(stmt)
                continue
        print("Skipping column: {} ({})".format(ia.key, ia.name))
    print('Done.\n')


########################################
# Integrity Helpers
########################################

def _strip_numeric_suffix(value):
    return re.sub(r'\d+$', '', value)


def _get_numeric_suffix(value):
    match = re.match(r'.*?(\d+)$', value)
    if match:
        return int(match.groups()[0])


def get_next_valid_name_with_numeric_suffix(current_name, name_col):
    name_wo_numeric_suffix = _strip_numeric_suffix(current_name)
    name_w_numeric_suffix_regex = r"{}[[:digit:]]+$".format(name_wo_numeric_suffix)

    matching_rows = db.session.query(name_col).filter(name_col.op('regexp')(name_w_numeric_suffix_regex)).all()
    name_suffixes_ordered = sorted(
        filter(None, [_get_numeric_suffix(x[0]) for x in matching_rows]))

    highest_suffix = 0
    if name_suffixes_ordered:
        highest_suffix = name_suffixes_ordered[-1]
    return name_wo_numeric_suffix + str(highest_suffix + 1)


########################################
# Debugging Helpers
########################################

def format_query_statement(statement, params, collapse_whitespace=True, collapse_select_clauses=True):
    """Format the provided SQL statement by substituting params and optionally collapsing the select clauses and
    repetitive whitespace.
    """
    if collapse_whitespace:
        statement = re.sub(WHITESPACE_RE, u' ', statement, re.U)

    if collapse_select_clauses:
        statement = re.sub(SELECT_CLAUSE_RE, u'SELECT ... FROM ', statement, re.U)

    try:
        statement = statement % params
    except (TypeError, UnicodeDecodeError):
        pass
    else:
        params = None

    return statement, params


def get_debug_queries_summary(debug_queries=None, collapse_whitespace=True, collapse_select_clauses=False):
    """Generate a summary of the SQL queries gathered by Flask-SQLAlchemy during the course of this request."""
    if debug_queries is None:
        debug_queries = get_debug_queries()
    r = []
    total_duration = 0
    for i, q in enumerate(sorted(debug_queries, key=lambda x: x.start_time)):
        total_duration += q.duration
        # Clean up query statement and substitute parameters
        stmt, params = format_query_statement(
            q.statement,
            q.parameters,
            collapse_whitespace=collapse_whitespace,
            collapse_select_clauses=collapse_select_clauses)

        # Construct the output buffer
        b = [u'-' * 80, u"Query #{}:".format(i + 1), u'> ' + stmt]
        if params:
            b.append(u"Params: {}".format(params))
        if q.context and q.context != '<unknown>':
            b.append(u"Context: {}".format(q.context))
        b.append(u"Duration: {}".format(q.duration))
        r.append(u'\n'.join(b))
    summary = [
        u"{border}\nQuery Summary\n{border}".format(border=(u'=' * 80)),
        u"Num Queries: {}".format(len(r)),
        u"Total Duration: {}".format(total_duration)
    ]
    return u'\n'.join(summary) + u'\n' + u'\n'.join(r)


def clear_debug_queries():
    """Clear the SQL queries gathered by Flask-SQLAlchemy."""
    ctx = connection_stack.top
    if ctx is not None:
        setattr(ctx, 'sqlalchemy_queries', [])


@contextmanager
def debug_queries_summary(collapse_whitespace=True, collapse_select_clauses=False):
    clear_debug_queries()
    yield
    print get_debug_queries_summary(
        collapse_whitespace=collapse_whitespace, collapse_select_clauses=collapse_select_clauses)


def __log_event(event_name, description=None, **info):
    print "\n** {} **".format(event_name)
    if description:
        print u'"{}"'.format(description)
    if 'statement' in info and 'parameters' in info:
        statement, _ = format_query_statement(info['statement'], info['parameters'])
        info['statement'] = statement
    pprint(info)


def _log_engine_event(event_name, **kwargs):
    __log_event("engine :: {}".format(event_name), **kwargs)


def _log_session_event(event_name, **kwargs):
    __log_event("session :: {}".format(event_name), **kwargs)


def _log_model_event(event_name, **kwargs):
    __log_event("model :: {}".format(event_name), **kwargs)


def attach_db_engine_event_debug_listeners(app, bind=None, include_execute_events=False):
    """Attach event listeners to the DB engine for this `app` and optional `bind`.
    :param include_execute_events: Bind events that involve SQL execution if True.
    """
    engine = db.get_engine(app, bind=bind)

    @event.listens_for(engine, 'first_connect')
    def on_first_connect(dbapi_connection, connection_record):
        _log_engine_event(
            'first_connect',
            description=u'First time a DBAPI connection is checked out from a particular Pool.',
            **locals())

    @event.listens_for(engine, 'connect')
    def on_connect(dbapi_connection, connection_record):
        _log_engine_event('connect', description=u'DBAPI connection is first created for a given Pool.', **locals())

    @event.listens_for(engine, 'checkout')
    def on_checkout(dbapi_connection, connection_record, connection_proxy):
        _log_engine_event('checkout', description=u'Connection is retrieved from the Pool.', **locals())

    @event.listens_for(engine, 'engine_connect')
    def on_engine_connect(conn, branch):
        _log_engine_event('engine_connect', description=u'Intercept the creation of a new Connection.', **locals())

    @event.listens_for(engine, 'begin')
    def on_begin(conn):
        _log_engine_event('begin', description=u'Intercept begin() events.', **locals())

    if include_execute_events:
        @event.listens_for(engine, 'before_execute', retval=False)
        def on_before_execute(conn, clauseelement, multiparams, params):
            # Receives uncompiled SQL constructs and other objects prior to rendering into SQL
            _log_engine_event(
                'before_execute',
                description=u'Intercept high level execute() events.',
                **locals())

        @event.listens_for(engine, 'before_cursor_execute', retval=False)
        def on_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            # Receives the string SQL statement and DBAPI-specific parameter list to be invoked against a cursor.
            _log_engine_event(
                'before_cursor_execute',
                description=u'Intercept low-level cursor execute() events before execution.',
                **locals())

        @event.listens_for(engine, 'after_cursor_execute')
        def on_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            _log_engine_event(
                'after_cursor_execute',
                description=u'Intercept low-level cursor execute() events after execution.',
                **locals())

        @event.listens_for(engine, 'after_execute')
        def on_after_execute(conn, clauseelement, multiparams, params, result):
            _log_engine_event(
                'after_execute',
                description=u'Intercept high level execute() events after execute.',
                **locals())

    @event.listens_for(engine, 'commit')
    def on_commit(conn):
        _log_engine_event(
            'commit', description=u'Intercept commit() events, as initiated by a Transaction.', **locals())

    @event.listens_for(engine, 'reset')
    def on_reset(dbapi_connection, connection_record):
        _log_engine_event('reset', description=u'Before the "reset" action occurs for a pooled connection.', **locals())

    @event.listens_for(engine, 'rollback')
    def on_rollback(conn):
        _log_engine_event(
            'rollback', description=u'Intercept rollback() events, as initiated by a Transaction.', **locals())

    @event.listens_for(engine, 'checkin')
    def on_checkin(dbapi_connection, connection_record):
        _log_engine_event('checkin', description=u'Connection returned to Pool.', **locals())

    @event.listens_for(engine, 'invalidate')
    def on_invalidate(dbapi_connection, connection_record, exception):
        _log_engine_event('invalidate', description=u'DBAPI connection is to be "invalidated.', **locals())

    @event.listens_for(engine, 'dbapi_error')
    def on_dbapi_error(conn, cursor, statement, parameters, context, exception):
        _log_engine_event('dbapi_error', description=u'Intercept a raw DBAPI error.', **locals())

    @event.listens_for(engine, 'release_savepoint')
    def on_release_savepoint(conn, name, context):
        _log_engine_event('release_savepoint', description=u'Intercept release_savepoint() events.', **locals())

    @event.listens_for(engine, 'rollback_savepoint')
    def on_rollback_savepoint(conn, name, context):
        _log_engine_event('rollback_savepoint', description=u'Intercept rollback_savepoint() events.', **locals())

    @event.listens_for(engine, 'savepoint')
    def on_savepoint(conn, name):
        _log_engine_event('savepoint', description=u'Intercept savepoint() events.', **locals())

    @event.listens_for(engine, 'set_connection_execution_options')
    def on_set_connection_execution_options(conn, opts):
        _log_engine_event(
            'set_connection_execution_options',
            description=u'Intercept when the Connection.execution_options() method is called.',
            **locals())

    @event.listens_for(engine, 'set_engine_execution_options')
    def on_set_engine_execution_options(engine, opts):
        _log_engine_event(
            'set_engine_execution_options',
            description=u'Intercept when the Engine.execution_options() method is called.',
            **locals())


def attach_db_session_event_debug_listeners(db_session):
    """Attach event listeners to the DB session that pertain to certain session lifecycle events like flush & commit."""

    @event.listens_for(type(db_session), 'after_attach')
    def on_after_attach(session, instance):
        _log_session_event(
            'after_attach',
            description=u'Execute after an instance is attached to a session.',
            **locals())

    @event.listens_for(type(db_session), 'after_begin')
    def on_after_begin(session, transaction, conn):
        _log_session_event(
            'after_begin', description=u'Execute after a transaction is begun on a connection.', **locals())

    @event.listens_for(type(db_session), 'after_commit')
    def on_after_commit(session):
        # Note that this may not be per-flush if a longer running transaction is ongoing.
        _log_session_event(
            'after_commit', description=u'Execute after a commit has occurred.', **locals())

    @event.listens_for(type(db_session), 'after_flush')
    def on_after_flush(session, flush_context):
        # Note that the session's state is still in pre-flush,
        # i.e. 'new', 'dirty', and 'deleted' lists still show pre-flush state
        # as well as the history settings on instance attributes.
        _log_session_event(
            'after_flush',
            description=u'Execute after flush has completed, but before commit has been called.',
            **locals())

    @event.listens_for(type(db_session), 'before_flush')
    def on_before_flush(session, flush_context, instances):
        info = locals()
        info['model_changes'] = session._model_changes
        _log_session_event('before_flush', **info)

    @event.listens_for(type(db_session), 'before_commit')
    def on_before_commit(session):
        _log_session_event('before_commit', **locals())


def attach_db_model_event_debug_listeners(app):
    """Attach event listeners to this `app` that pertain to certain model lifecycle events like state changes."""

    @sqla.before_models_committed.connect_via(app)
    def on_before_models_committed(sender, changes):
        # NOTE: Doesn't seem to fire if a flush wasn't issued prior to the commit!
        _log_model_event(sqla.before_models_committed.name, **locals())

    @sqla.models_committed.connect_via(app)
    def on_models_committed(sender, changes):
        _log_model_event(sqla.models_committed.name, **locals())
