from app import db
import time


class User(db.Model):

    __tablename__ = 'user'
    userId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    project = db.relationship('Project', back_populates='user')

    def __repr__(self):
        return self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.userId

    def to_dict(self):
        return {
            "userId": self.userId,
            "email": self.email,
            "username": self.username
        }


class Project(db.Model):

    __tablename__ = 'project'
    projectId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    p_name = db.Column(db.String(20), nullable=False)
    p_desc = db.Column(db.String(50))
    status = db.Column(db.Boolean(), default=True)
    creator = db.Column(db.Integer(), db.ForeignKey('user.userId'))

    user = db.relationship('User', back_populates='project')
    module = db.relationship('Module', back_populates='project')
    api = db.relationship('Api', back_populates='project')

    def __repr__(self):
        return self.p_name

    def create(self):
        # 创建方法
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            "projectId": self.projectId,
            "p_name": self.p_name,
            "p_desc": self.p_desc,
            "creator": self.creator,
            "status": self.status
        }

    @classmethod
    def find_by_name(cls, name, status=True):
        return cls.query.filter_by(p_name=name, status=status).first()

    @classmethod
    def find_by_id(cls, projectId):
        return cls.query.filter_by(projectId=projectId).first()


class Module(db.Model):

    __tablename__ = 'module'
    moduleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    m_name = db.Column(db.String(50), nullable=False)
    m_desc = db.Column(db.String(100))
    project_id = db.Column(db.Integer, db.ForeignKey('project.projectId'))
    creator = db.Column(db.Integer, db.ForeignKey('user.userId'))
    status = db.Column(db.Boolean, default=True)

    project = db.relationship('Project', back_populates='module')
    api = db.relationship('Api', back_populates='module')

    def __repr__(self):
        return self.m_name

    def create(self):
        # 创建方法
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            "moduleId": self.moduleId,
            "m_name": self.m_name,
            "m_desc": self.m_desc,
            "creator": self.creator,
            "project_id": self.project_id
        }

    @classmethod
    def find_by_name(cls, name, status=True):
        return cls.query.filter_by(m_name=name, status=status).first()

    @classmethod
    def find_by_id(cls, moduleId, status=True):
        return cls.query.filter_by(moduleId=moduleId, status=status).first()

    @classmethod
    def get_modules_of_project(cls, projectId):
        return cls.query.filter_by(project_id=projectId, status=True).all()


class Api(db.Model):

    __tablename__ = 'api'
    apiId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_name = db.Column(db.String(50), nullable=False)
    a_desc = db.Column(db.String(100))
    a_method = db.Column(db.String(10), nullable=False)
    a_url = db.Column(db.String(500), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.moduleId'))
    # creator = db.Column(db.Integer, db.ForeignKey('user.userId'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.projectId'))
    creator = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=True)

    module = db.relationship('Module', back_populates='api')
    project = db.relationship('Project', back_populates='api')
    case = db.relationship('Case', back_populates='api')

    def __repr__(self):
        return self.a_name

    def create(self):
        # 创建方法
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            "apiId": self.apiId,
            "a_name": self.a_name,
            "a_desc": self.a_desc,
            "a_method": self.a_method,
            "project_id": self.project_id,
            "module_id": self.module_id,
            "creator": self.creator,
            "status": self.status
        }

    @classmethod
    def find_by_id(cls, apiId, status=True):
        return cls.query.filter_by(apiId=apiId, status=status).first()


class Case(db.Model):

    __tablename__ = 'case'
    caseId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(50), nullable=False)
    c_desc = db.Column(db.String(100))
    setup = db.Column(db.String(20), default='[]')
    teardown = db.Column(db.String(20), default='[]')
    c_body = db.Column(db.Text)
    c_header = db.Column(db.Text)
    c_query = db.Column(db.String(500))
    c_assert = db.Column(db.String(200))
    c_save_param = db.Column(db.String(100))
    creator = db.Column(db.Integer)
    api_id = db.Column(db.Integer, db.ForeignKey('api.apiId'))
    status = db.Column(db.Boolean, default=True)

    api = db.relationship('Api', back_populates='case')

    def __repr__(self):
        return self.c_name

    def create(self):
        # 创建方法
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            "caseId": self.caseId,
            "c_name": self.c_name,
            "c_desc": self.c_desc,
            "setup": self.setup,
            "teardown": self.teardown,
            "c_header": self.c_header,
            "c_body": self.c_body,
            "c_query": self.c_query,
            "c_assert": self.c_assert,
            "c_save_param": self.c_save_param,
            "creator": self.creator,
            "status": self.status
        }

    @classmethod
    def find_by_id(cls, caseId, status=True):
        return cls.query.filter_by(caseId=caseId, status=status).first()


class Task(db.Model):

    __tablename__ = 'task'
    taskId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(50))
    t_desc = db.Column(db.String(100))
    t_startAt = db.Column(db.DateTime)
    t_endAt = db.Column(db.DateTime)
    t_apis = db.Column(db.Text)
    t_result = db.Column(db.Text)

    result = db.relationship('Result', backref='task', lazy='dynamic')

    def __repr__(self):
        return self.t_name

    def create(self):
        # 创建方法
        db.session.add(self)
        db.session.commit()
        return self


class Result(db.Model):
    __tablename__ = 'result'
    resultId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    r_time = db.Column(db.DateTime)
    r_content = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('task.taskId'))

    # def __repr__(self):
    #     return self

    def create(self):
        # 创建方法
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            "resultId": self.resultId,
            "taskId": self.task_id,
            "time": self.r_time,
            "content": self.r_content
        }