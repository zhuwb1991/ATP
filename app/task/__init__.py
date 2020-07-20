from flask import Blueprint

task = Blueprint('task', __name__, url_prefix='/api')

from . import views

