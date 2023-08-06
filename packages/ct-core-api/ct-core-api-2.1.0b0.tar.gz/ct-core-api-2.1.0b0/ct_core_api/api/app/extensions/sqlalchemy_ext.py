import sys

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

from ct_core_db.lib import db_utils as dbu
from ct_core_api.core.database import db


def init_app(app):
    force_auto_coercion()
    force_instant_defaults()

    # Only configure the SQLAlchemy DB extension if a connection URI is set
    if bool(app.config.get('SQLALCHEMY_DATABASE_URI')):
        db.configure_mappers()
        db.init_app(app)

        # Optionally attach SQLAlchemy event listeners to log debug messages
        if app.config.get('SQLA_EVENT_DEBUG_LOGGING'):
            include_execute_events = app.config.get('SQLA_EXECUTE_EVENT_DEBUG_LOGGING', False)
            dbu.attach_db_engine_event_debug_listeners(app, include_execute_events=include_execute_events)
            dbu.attach_db_model_event_debug_listeners(app)
            dbu.attach_db_session_event_debug_listeners(db.session)

        # Prevent `InvalidRequestError`s by rolling back when SQLAlchemy raises
        if not app.propagate_exceptions:
            @app.errorhandler(SQLAlchemyError)
            def handle_sqla_error(exc):
                db.session.rollback()
                exc_type, exc_value, tb = sys.exc_info()
                raise exc_type, exc_value, tb
