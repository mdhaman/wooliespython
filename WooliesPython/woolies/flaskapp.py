import os
import importlib
from flask import Flask

WOOLIES_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app(config=None):
    # instantiate flask app
    app = Flask(__name__)
    # load the default_setting
    app.config.from_pyfile(os.path.join(WOOLIES_DIR, 'default_settings.py'))

    # if the config override is provided use that.
    if config:
        app.config.update(config)

    def install_app(module_name):
        app_module = importlib.import_module(module_name)
        if hasattr(app_module, 'init_app'):
            app_module.init_app(app)

    def setup_blueprints(module_name):
        """Setup configured blueprints."""
        app_module = importlib.import_module(module_name)
        if hasattr(app_module, 'blueprint'):
            app.register_blueprint(app_module.blueprint)

    for module_name in app.config.get('BLUEPRINTS', []):
        setup_blueprints(module_name)

    for module_name in app.config.get('INSTALLED_APPS', []):
        install_app(module_name)

    return app

