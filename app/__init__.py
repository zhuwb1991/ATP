from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# from flask_login import LoginManager
from .config import config


app = Flask(__name__)

app.config.from_object(config['development'])

# login_manager = LoginManager(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

from . import models
from app.user import user
from app.project import project
from app.module import module
from app.api import interface
from app.case import case
from app.task import task

app.register_blueprint(user)
app.register_blueprint(project)
app.register_blueprint(module)
app.register_blueprint(interface)
app.register_blueprint(case)
app.register_blueprint(task)
