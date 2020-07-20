from app.models import Task


def get_cases_of_task(taskId):
    # 获取任务的所有用例列表
    db_task = Task.query.filter_by(taskId=taskId).first()
    apis = db_task.t_apis

    return eval(apis)