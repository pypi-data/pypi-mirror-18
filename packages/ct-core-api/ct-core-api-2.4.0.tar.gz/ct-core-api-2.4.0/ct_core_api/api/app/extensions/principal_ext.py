from flask_principal import Principal

# Don't use sessions to extract and store identification; ignore static endpoints.
principal = Principal(use_sessions=False, skip_static=True)


def init_app(app):
    principal.init_app(app)
    app.register_extension(principal, 'flask-principal')
