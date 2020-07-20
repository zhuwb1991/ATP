from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app.models import User, Project, Module, Api, Case, Task, Result

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Project=Project, Module=Module, Api=Api, Case=Case, Task=Task, Result=Result)


manager.add_command('Shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
