import os

from ct_core_api.api.app import APIApp

CONFIG_NAME_MAPPER = {
    'development': 'ct_core_api.api.app.config.DevelopmentConfig',
    'testing': 'ct_core_api.api.app.config.TestingConfig',
    'production': 'ct_core_api.api.app.config.ProductionConfig'}


########################################
# API Application Factory
########################################

def load_configs(app, flask_config_name=None, config=None, **config_kwargs):
    # 1) Load config object by name from `flask_config_name` or the `FLASK_CONFIG` environment variable
    config_name = flask_config_name or os.getenv('FLASK_CONFIG', 'production')
    app.config.from_object(CONFIG_NAME_MAPPER[config_name])

    # 2) Load the provided `config` object
    if config:
        app.config.from_object(config)

    # 3) Load instance relative config (settings.cfg)
    app.config.from_pyfile('settings.cfg', silent=True)

    # 4) Overwrite config with keyword arguments
    for k, v in config_kwargs.iteritems():
        if k in app.config:
            app.logger.info("Overwriting config value: {} = {!r}".format(k, v))
        else:
            app.logger.info("Setting config value: {} = {!r}".format(k, v))
        app.config[k] = v


def create_api_app(import_name, flask_config_name=None, config=None, **kwargs):
    # Uppercase keys are considered config properties
    config_kwargs = {k: v for k, v in kwargs.iteritems() if k.isupper()}
    kwargs = {k: v for k, v in kwargs.iteritems() if not k.isupper()}

    app = APIApp(import_name, **kwargs)
    load_configs(app, flask_config_name, config, **config_kwargs)

    from ct_core_api.api.app import logging
    logging.init_app(app)

    from ct_core_api.api.app import debugging
    debugging.init_app(app)

    from ct_core_api.api.app import extensions
    extensions.init_app(app)

    from ct_core_api.api.app import templating
    templating.init_app(app)

    from ct_core_api.api.app import commands
    commands.init_app(app)

    from ct_core_api.api.app import modules
    modules.init_app(app)

    return app
