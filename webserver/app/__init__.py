from flask import Flask, jsonify
from flask_injector import FlaskInjector
from .modules import AppModule
from .extensions import db
from dotenv import load_dotenv

load_dotenv()

def create_app(config='app.config.DevConfig', injector_modules=None):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .users.routes import users_bp
    from .auth.routes import auth_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({'error': 'Forbidden', 'reason': str(e)}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found', 'reason': str(e)}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'Method not allowed', 'reason': str(e)}), 405

    # use provided modules (e.g. test mocks) or fall back to real AppModule
    modules = injector_modules if injector_modules is not None else [AppModule(app)]
    FlaskInjector(app=app, modules=modules)

    return app