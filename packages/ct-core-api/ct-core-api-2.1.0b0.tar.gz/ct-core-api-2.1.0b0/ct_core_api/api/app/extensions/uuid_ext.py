from flask_uuid import FlaskUUID


def init_app(app):
    flask_uuid = FlaskUUID(app)
    app.register_extension(flask_uuid, 'flask-uuid')
