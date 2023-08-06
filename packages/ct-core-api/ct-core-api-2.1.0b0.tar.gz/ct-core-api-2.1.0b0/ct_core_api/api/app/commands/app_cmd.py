import importlib
import os
import pkgutil

from flask import Flask
from texttable import Texttable


def init_app(app):
    @app.cli.command(name='app')
    def app_cmd():
        """Display application information."""
        available_apps = []

        # Locate available apps
        apps_path = app.config.get('APPS_PATH')
        if apps_path:
            apps_pkg = apps_path.replace('/', '.')
            try:
                for app_module_name in ['.'.join([apps_pkg, name]) for _, name, _ in pkgutil.iter_modules([apps_path])]:
                    app_module = importlib.import_module(app_module_name)
                    a = getattr(app_module, 'app')
                    if isinstance(a, Flask) and a.name != app.name:
                        app_module_path = "{}.py".format(app_module_name.replace('.', '/'))
                        available_apps.append((a.name, app_module_path))
            except ImportError:
                print("Unable to import application modules from: {}\n".format(apps_pkg))

        # Environment Variables
        table = Texttable()
        table.add_rows([
            ('Environment', 'Variables'),
            ('FLASK_APP', os.environ.get('FLASK_APP', '<unset>')),
            ('FLASK_DEBUG', os.environ.get('FLASK_DEBUG', '<unset>')),
            ('FLASK_CONFIG', os.environ.get('FLASK_CONFIG', '<unset>'))])
        print(table.draw())

        # Current Flask App
        print('')
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.add_rows([
            ('App (Current)',),
            (app.name + ' [debug]' if app.debug else '',)])
        print(table.draw())

        # Available Flask App(s)
        if available_apps:
            print
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.add_rows(
                [('Apps (Available)', '')] +
                [(aa[0], "export FLASK_APP={}".format(aa[1])) for aa in available_apps])
            print(table.draw())

        # App Extensions
        print('')
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.add_rows(
            [('App Extensions',)] +
            [(x,) for x in sorted(getattr(app, 'extensions', {}).keys())])
        print(table.draw())

        print('')
        table = Texttable(max_width=0)
        table.set_cols_align(["l", "r"])
        table.set_deco(Texttable.HEADER)
        table.add_rows(
            [('App Routes', 'Request Method(s)')] +
            [("{} - [{}]".format(x.rule, x.endpoint), ' '.join(
                sorted(x.methods, key=lambda y: 'GET PATCH PUT POST DELETE HEAD OPTIONS'.split().index(y))))
                for x in sorted(app.url_map.iter_rules(), key=lambda y: (y.rule, y.endpoint))])
        print(table.draw())
