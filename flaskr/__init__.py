import os

from flask import Flask
#from . import db

def create_app(test_config=None):
    """Create and configure an instance of the Flask
    application.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # A default secret that should be overridden by instance
        # config
        SECRET_KEY='dev',
        # Store the db in the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Register the db commands
    from flaskr import db

    db.init_app(app)

    # Apply blueprints to the app
    from flaskr import auth, blog
    app.register_blueprint(auth.bp)
    # from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index') # Blog blueprint doesn't have a url_prefix, so index is at /

    return app