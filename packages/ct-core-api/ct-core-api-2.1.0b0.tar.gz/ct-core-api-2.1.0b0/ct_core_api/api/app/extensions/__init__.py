"""
Extensions
==========
Extensions provide access to common resources of the application.
"""


def init_app(app):
    from importlib import import_module
    for module_name in app.config['ENABLED_EXTENSIONS']:
        import_module(".{}".format(module_name), package=__name__).init_app(app)
