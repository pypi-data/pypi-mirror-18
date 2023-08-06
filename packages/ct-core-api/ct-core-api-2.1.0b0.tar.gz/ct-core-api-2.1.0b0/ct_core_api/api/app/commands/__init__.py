"""
Commands
========
Flask commands provide CLI tools for managing the application and its data.
"""
from ct_core_api.api.app.commands import app_cmd, db_cmd, shell_cmd


def init_app(app):
    for command in (shell_cmd, db_cmd, app_cmd):
        command.init_app(app)
