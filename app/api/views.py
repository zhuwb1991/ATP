from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app import db
from app.models import Project, User, Module, Api
from . import interface


class InterfaceView(MethodView):

    @jwt_required
    def get(self):
        # 根据查询条件获取接口列表
        project_id = request.args.get("projectId", 0)
        module_id = request.args.get("moduleId", 0)
        pagenum = request.args.get("pagenum")
        pagesize = request.args.get("pagesize")

        # TODO 参数类型判断
        apis = None
        if project_id == 0 and module_id == 0:
            # 查询全部接口
            apis = Api.query.filter_by(status=True)
        if project_id == 0 and module_id != 0:
            # 根据moduleId查询接口
            apis = Api.query.filter_by(module_id=module_id, status=True)
        if project_id != 0 and module_id == 0:
            # 根据projectId查询接口
            apis = Api.query.filter_by(project_id=project_id, status=True)
        if project_id != 0 and module_id != 0:
            # 根据projectId和moduleId查询接口
            apis = Api.query.filter_by(project_id=project_id, module_id=module_id, status=True)

        query = apis.paginate(int(pagenum), int(pagesize), error_out=False)
        result = []

        for i in query.items:
            result.append(i.to_dict())

        total = apis.count()

        return jsonify({
            "code": 200,
            "msg": "获取项目列表成功",
            "data": {
                "apis": result,
                "total": total
            }
        })

    @jwt_required
    def post(self):
        # 创建接口

        form = request.get_json()
        name = form.get('a_name', '')
        desc = form.get('a_desc', '')
        method = form.get('a_method', 'GET')
        url = form.get('a_url', '')
        module_id = form.get('moduleId', 0)
        project_id = form.get('projectId', 0)

        if not name or not module_id or not project_id or not url:
            return jsonify({"code": 400, "msg": "参数错误"})

        userId = get_jwt_identity()
        new_api = Api(a_name=name, a_desc=desc, a_method=method, a_url=url,
                      module_id=module_id, project_id=project_id, creator=userId)

        try:
            new_api.create()
            return jsonify({"code": 201, "msg": "创建接口成功"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 400, "msg": e})
        finally:
            db.session.close()


@interface.route('/interface/<int:apiId>', methods=["PUT"])
@jwt_required
def modify_api(apiId):

    form = request.get_json()
    name = form.get('a_name', '')
    desc = form.get('a_desc', '')
    method = form.get('a_method', 'GET')
    url = form.get('a_url', '')

    # 查询数据库中apiId=apiId的项目信息
    db_api = Api.find_by_id(apiId)
    if not db_api:
        return jsonify({"code": 404, "msg": "apiId不存在"})

    db_api.a_name = name
    db_api.a_desc = desc
    db_api.a_method = method
    db_api.a_url = url
    try:
        db.session.commit()
        return jsonify({'msg': '编辑成功', 'code': 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e), 'code': 500})
