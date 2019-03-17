from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/api')

from . import views
from woolies.woolies_api_client import ApiClient

def init_app(app):
    app.woolies_api = ApiClient(app.config.get('WOOLIES_BASE_URL'), app.config.get('TOKEN'))
