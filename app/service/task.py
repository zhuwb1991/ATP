from app.service.case import Case as C
from app.service.db_service import get_cases_of_task
from app.models import Result
import time


class Task:

    def __init__(self, task_id):
        self.task_id = task_id
        self.case_list = self.get_case_list(task_id)
        self.result = []

    def get_case_list(self, id):
        return get_cases_of_task(id)

    def start(self):
        print(self.case_list)
        for i in self.case_list:
            c = C(i)
            c.run()
            self.result.append({
                "case_id": i,
                "case_result": c.res
            })
            print("用例：%d 执行完成====================" % i)

        print(self.result)
        new_result = Result(r_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), task_id=self.task_id, r_content=str(self.result))
        new_result.create()


if __name__ == '__main__':

    t = Task(1)
    t.start()
