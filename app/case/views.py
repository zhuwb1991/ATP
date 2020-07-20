from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Project, User, Module, Api, Case
from . import case


@case.route('/interface/<int:apiId>/cases', methods=["GET"])
@jwt_required
def get_case_list(apiId):
    # 根据接口获取用例列表
    pagenum = request.args.get("pagenum")
    pagesize = request.args.get("pagesize")

    # TODO 参数类型判断
    cases = Case.query.filter_by(api_id=apiId, status=True)

    query = cases.paginate(int(pagenum), int(pagesize), error_out=False)
    result = []

    for i in query.items:
        result.append(i.to_dict())

    total = cases.count()

    return jsonify({
        "code": 200,
        "msg": "获取用例列表成功",
        "data": {
            "cases": result,
            "total": total
        }
    })


@case.route('/cases', methods=["POST"])
@jwt_required
def create_case():
    # 创建用例

    form = request.get_json()
    name = form.get('c_name', '')
    desc = form.get('c_desc', '')
    setup = form.get('setup', '[]')
    teardown = form.get('teardown', '[]')
    params = form.get('c_query', '')
    headers = form.get('c_header', '')
    body = form.get('c_body', '')
    asserts = form.get('c_assert', '')
    tmp_param = form.get('c_save_param', '')
    api_id = form.get('api_id')

    if not name or not api_id:
        return jsonify({"code": 400, "msg": "参数错误"})

    userId = get_jwt_identity()
    new_case = Case(c_name=name, c_desc=desc, setup=str(setup), teardown=str(teardown), c_query=params, c_body=str(body),
                    c_header=str(headers), c_assert=str(asserts), c_save_param=tmp_param, api_id=api_id, creator=userId)

    try:
        new_case.create()
        return jsonify({"code": 201, "msg": "创建用例成功"})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"code": 400, "msg": str(e)})
    finally:
        db.session.close()


@case.route('/cases/<int:caseId>', methods=["PUT"])
@jwt_required
def modify_case(caseId):

    form = request.get_json()
    name = form.get('c_name', '')
    desc = form.get('c_desc', '')
    setup = form.get('setup', None)
    teardown = form.get('teardown', None)
    params = form.get('c_query', '')
    headers = form.get('c_header', '')
    body = form.get('c_body', '')
    asserts = form.get('c_assert', '')
    tmp_param = form.get('c_save_param', '')

    # 查询数据库中apiId=apiId的项目信息
    db_case = Case.find_by_id(caseId)
    if not db_case:
        return jsonify({"code": 400, "msg": "caseId不存在"})

    db_case.c_name = name
    db_case.c_desc = desc
    db_case.setup = str(setup)
    db_case.teardown = str(teardown)
    db_case.c_query = params
    db_case.c_header = str(headers)
    db_case.c_body = str(body)
    db_case.c_assert = str(asserts)
    db_case.c_save_param = tmp_param
    try:
        db.session.commit()
        return jsonify({'msg': '编辑成功', 'code': 200})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e), 'code': 500})


@case.route('/cases/<int:caseId>/info')
def get_case_info(caseId):
    # 获取一个用例的详情，包含从api中的url, method
    case_info = case_detail(caseId)
    return jsonify({
        "code": 200,
        "msg": "",
        "data": case_info
    })


def case_detail(caseId):
    db_case = Case.find_by_id(caseId)
    api = db_case.api

    case_info = {
        **db_case.to_dict(),
        "url": api.a_url,
        "method": api.a_method
    }
    return case_info
