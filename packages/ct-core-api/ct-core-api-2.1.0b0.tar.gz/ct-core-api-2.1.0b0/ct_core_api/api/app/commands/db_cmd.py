import logging
import os

import click

from ct_core_api.core.database import db as db_instance
from ct_core_db.lib import mysql_diff, mysql_version

_logger = logging.getLogger(__name__)


########################################
# DB Commands
########################################

class DBCommandSettings(object):
    MYSQL_DIFF_PATH = 'MYSQL_DIFF_PATH'
    VERSIONS_DIR = 'DB_VERSIONS_DIR'
    VERSIONS_TABLE_NAME = 'DB_VERSIONS_TABLE_NAME'


def init_app(app, db=None, bind=None):
    # Don't register the `db` command if a connection URI isn't set
    if not bool(app.config.get('SQLALCHEMY_DATABASE_URI')):
        return

    db = db or db_instance
    engine = db.get_engine(app, bind=bind)
    db_manager = mysql_version.DBManager(mysql_version.SQLConnector(engine))

    @app.cli.group('db')
    def cli():
        """DB management commands."""
        pass

    @cli.command()
    def info():
        """Print the info banner."""
        db_manager.print_info()

    @cli.command()
    def create():
        """Create tables for db models."""
        db_manager.create_db(db.metadata)

    @cli.command()
    def drop():
        """Drop tables for db models."""
        db_manager.drop_db(db.metadata)

    if engine.name == 'mysql':
        # Initialize the MySQL Version Manager
        mysql_diff_path = app.config.get(DBCommandSettings.MYSQL_DIFF_PATH)
        mysql_diff_cmd = mysql_diff.MySQLDiffCommand(mysql_diff_path)
        versions_dir = (
            app.config.get(DBCommandSettings.VERSIONS_DIR) or
            mysql_version.MySQLVersionManager.DEFAULT_DB_VERSIONS_DIR)
        versions_dir = os.path.relpath(os.path.join(app.root_path, '..', versions_dir))
        version_table_name = app.config.get(DBCommandSettings.VERSIONS_TABLE_NAME)
        db_version_manager = mysql_version.MySQLVersionManager(engine, mysql_diff_cmd, versions_dir, version_table_name)

        @cli.command()
        def upgrade():
            """Upgrade the database schema."""
            db_version_manager.upgrade_db()

        @cli.command()
        def update():
            """Upgrade the database schema."""
            db_version_manager.upgrade_db()

        @cli.command()
        @click.option('--baseline-version', '-v')
        def init(baseline_version=None):
            """Create and apply the baseline upgrade script."""
            db_version_manager.init_db(baseline_version)

        @cli.command()
        @click.option('--comment', '-c', help='A comment to include in the generated SQL script.')
        @click.option('--preview/--no-preview', default=False, help='Show the generated SQL statements.')
        def diff(comment=None, preview=False):
            """Diff the db schema and create upgrade script."""
            db_version_manager.diff_db(db.metadata, comment, preview)
