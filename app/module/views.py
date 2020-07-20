from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app import db
from app.models import Project, User, Module
from . import module


class ModuleView(MethodView):

    @jwt_required
    def get(self):
        pagenum = request.args.get("pagenum")
        pagesize = request.args.get("pagesize")

        # TODO 参数类型判断
        modules = Module.query.filter_by(status=True)
        query = modules.paginate(int(pagenum), int(pagesize), error_out=False)
        result = []

        for i in query.items:
            result.append(i.to_dict())
        total = modules.count()

        return jsonify({
            "code": 200,
            "msg": "获取模块列表成功",
            "data": {
                "modules": result,
                "total": total
            }
        })

    @jwt_required
    def post(self):
        # 创建模块

        data = request.get_json()
        name = data.get('m_name', '')
        desc = data.get('m_desc', '')
        project_id = data.get('projectId', 0)

        if not name or not project_id:
            return jsonify({"code": 400, "msg": "参数错误"})

        # 判断项目是否存在
        if not Project.find_by_id(project_id):
            return jsonify({"code": 400, "msg": "projectId不存在"})
        # 查询数据库判断该项目是否存在这个名称的模块
        db_project = Module.query.filter_by(m_name=name, project_id=project_id, status=True).first()
        if db_project:
            return jsonify({'msg': '模块名已存在', 'code': 400})

        userId = get_jwt_identity()
        new_module = Module(m_name=name, m_desc=desc, creator=userId, project_id=project_id)

        try:
            new_module.create()
            return jsonify({"code": 201, "msg": "创建模块成功"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 400, "msg": e})
        finally:
            db.session.close()


@jwt_required
@module.route('/projects/<int:projectId>/modules/<int:moduleId>', methods=["PUT"])
def modify_module(projectId, moduleId):

    data = request.get_json()
    name = data['m_name']
    desc = data['m_desc']

    # 查询数据库中moduleId=moduleId的模块信息
    db_module = Module.find_by_id(moduleId)
    if not db_module:
        return jsonify({"code": 400, "msg": "moduleId不存在"})
    # 通过修改后的name查询数据库中是否已经存在
    db_module2 = Module.query.filter_by(project_id=projectId, m_name=name, status=True).first()
    # 如果修改后的name已经存在且不是本身
    if db_module2 and db_module2.moduleId != moduleId:
        return jsonify({'msg': '已存在{}模块'.format(name), 'code': 400})

    db_module.m_name = name
    db_module.m_desc = desc
    try:
        db.session.commit()
        return jsonify({'msg': '编辑成功', 'code': 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': e, 'code': 500})
