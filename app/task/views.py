from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task, Result
from . import task
from app.service.task import Task as T


@task.route('/tasks')
@jwt_required
def get_tasks():
    pass


@task.route('/tasks', methods=["POST"])
@jwt_required
def create_task():
    form = request.get_json()
    name = form.get('t_name', '')
    desc = form.get("t_desc", "")
    apis = form.get("t_apis", "")

    if not name or not apis:
        return jsonify({"code": 400, "msg": "参数错误"})

    # userId = get_jwt_identity()
    new_task = Task(t_name=name, t_desc=desc, t_apis=str(apis))

    try:
        new_task.create()
        return jsonify({"code": 201, "msg": "创建任务成功"})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"code": 400, "msg": str(e)})
    finally:
        db.session.close()


@task.route('/tasks/<int:taskId>', methods=["POST"])
def run_task(taskId):

    t = T(taskId)
    t.start()

    return jsonify({"code": 200, "msg": "任务开始成功，请耐心等待"})


@task.route('/tasks/<int:taskId>/results', methods=['GET'])
def get_result(taskId):

    print(taskId)
    results = Result.query.filter_by(task_id=taskId).first()
    # print(results)
    content = results.to_dict()
    res = content.get('content')
    res = eval(res)
    print(res)
    # res = res[0].get("case_result").get("Response")
    # print(res)
    return jsonify({"code": 200})
