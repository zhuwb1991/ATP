from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app import db
from app.models import Project, User, Module
from . import project


class ProjectView(MethodView):

    @jwt_required
    def get(self):
        pagenum = request.args.get("pagenum")
        pagesize = request.args.get("pagesize")

        # TODO 参数类型判断
        projects = Project.query.filter_by(status=True)
        query = projects.paginate(int(pagenum), int(pagesize), error_out=False)
        result = []

        for i in query.items:
            result.append(i.to_dict())
            print(i.user)
        total = projects.count()

        return jsonify({
            "code": 200,
            "msg": "获取项目列表成功",
            "data": {
                "projects": result,
                "total": total
            }
        })

    @jwt_required
    def post(self):
        # 创建项目

        data = request.get_json()
        name = data['p_name']
        desc = data['p_desc']

        if name == '':
            return jsonify({'msg': '项目名不能为空', 'code': 101})

        # 查询数据库判断是否项目已存在
        db_project = Project.query.filter_by(p_name=name, status=True).first()
        if db_project:
            return jsonify({'msg': '项目名已存在', 'code': 400})

        userId = get_jwt_identity()
        new_project = Project(p_name=name, p_desc=desc, creator=userId)

        try:
            new_project.create()
            return jsonify({"code": 201, "msg": "创建项目成功"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 400, "msg": e})
        finally:
            db.session.close()


@project.route('/projects/<int:projectId>', methods=["PUT"])
@jwt_required
def modify_project(projectId):

    data = request.get_json()
    name = data['p_name']
    desc = data['p_desc']

    # 查询数据库中projectId=projectId的项目信息
    db_project = Project.find_by_id(projectId)
    if not db_project:
        return jsonify({"code": 404, "msg": "projectId不存在"})
    # 通过修改后的name查询数据库中是否已经存在
    db_project2 = Project.find_by_name(name)
    # 如果修改后的name已经存在且不是本身
    if db_project2 and db_project2.projectId != projectId:
        return jsonify({'msg': '已存在{}项目'.format(name), 'code': 400})

    db_project.p_name = name
    db_project.p_desc = desc
    try:
        db.session.commit()
        return jsonify({'msg': '编辑成功', 'code': 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': e, 'code': 500})


@project.route('/projects/<int:projectId>/modules')
@jwt_required
def get_modules_of_project(projectId):

    modules = Module.get_modules_of_project(projectId)
    result = []
    for i in modules:
        result.append(i.to_dict())

    return jsonify({
        "code": 200,
        "msg": "获取模块列表成功",
        "data": {
            "modules": result,
        }
    })
