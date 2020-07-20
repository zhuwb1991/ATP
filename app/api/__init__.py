from flask import Blueprint

interface = Blueprint('api', __name__, url_prefix='/api')

from . import urls, views
