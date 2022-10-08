import os
from aplication import dbc

from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='aplication/static', template_folder='aplication/templates')
    app.config.from_mapping(
        SECRET_KEY = dbc.SEC,
        DATABASE = os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from aplication import db
    db.init_app(app)
    
    from aplication import auth
    app.register_blueprint(auth.bp)
    
    from aplication import inbox
    app.register_blueprint(inbox.bp)
    app.add_url_rule('/index', endpoint='auth.register')
    app.add_url_rule('/index.html', endpoint='auth.register')
    app.add_url_rule('/', endpoint='auth.register')

    return app