from flask import Blueprint

project = Blueprint('project', __name__, url_prefix='/api')

from . import urls, views
