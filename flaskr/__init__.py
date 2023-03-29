import os
from flask import redirect, render_template
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
migrate = Migrate()
moment = Moment()
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="DEV",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),)
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)

    # BluePrint Area
    @app.route('/')
    def index():
        return render_template('nav/index.j2')
    
    @app.route('/blog')
    def blog():
        return render_template('nav/blog.j2')
    
    @app.route('/life')
    def life():
        return render_template('nav/life.j2')
    
    @app.route('/about_me')
    def about_me():
        return render_template('nav/about_me.j2')
    
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from .blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    
    return app