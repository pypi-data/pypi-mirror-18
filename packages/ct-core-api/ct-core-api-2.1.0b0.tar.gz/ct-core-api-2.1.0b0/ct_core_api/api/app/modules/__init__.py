"""
Modules
=======
Modules enable logical resource separation.
You may control enabled modules by modifying the ``ENABLED_MODULES`` config setting.
"""


def init_app(app, **kwargs):
    from importlib import import_module
    for module_name in app.config['ENABLED_MODULES']:
        import_module(".{}".format(module_name), package=__name__).init_app(app, **kwargs)
