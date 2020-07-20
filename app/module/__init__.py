from flask import Blueprint

module = Blueprint('module', __name__, url_prefix='/api')

from . import urls, views
