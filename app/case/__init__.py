from flask import Blueprint

case = Blueprint('case', __name__, url_prefix='/api')

from . import views