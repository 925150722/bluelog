
import os
import click
from flask import Flask, render_template
from bluelog.settings import config
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.extensions import bootstrap, db, mail, ckeditor, moment


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)

    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='admin')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400


def register_commands(app):

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of category, default is 10.')
    @click.option('--post', default=50, help='Quantity of post, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comment, default is 500.')
    def forge(category, post, comment):
        from bluelog.fakes import fake_admin, fake_category, fake_comment, fake_post
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_category(category)

        click.echo('Generating %d categories...' % post)
        fake_post(post)

        click.echo('Generating %d categories...' % comment)
        fake_comment(comment)

        click.echo('Done.')

