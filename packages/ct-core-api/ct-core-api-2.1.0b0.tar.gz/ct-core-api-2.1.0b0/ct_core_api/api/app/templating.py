import os

import jinja2


def init_app(app):
    choice_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.relpath(__file__)), 'templates'))])
    app.jinja_loader = choice_loader
