import requests
from app.case.views import *
from app.utils.replace import *


class Case:

    def __init__(self, case_id):
        self.id = case_id
        self.session = requests.Session()
        self.case_param = {}
        self.case = self.get_case_info(case_id)
        self.setup = eval(self.case.get("setup"))
        self.teardown = eval(self.case.get("teardown", []))
        self.res = None

    def get_case_info(self, id):
        return case_detail(id)

    def run(self):
        print("执行用例：%d" % self.id)
        # 前置步骤
        if self.setup:
            print("用例的前置步骤有：%s" % self.setup)
            for i in self.setup:
                a = Api(i, self.session, self.case_param)
                a.request()
                # 保存临时参数
                self.case_param = a.params

        print("当前用例的步骤id： %d" % self.id)
        b = Api(self.id, self.session, self.case_param)
        b.request()
        self.res = b.asserts()
        # 保存临时参数
        self.case_param = b.params
        # 后置操作
        if self.teardown:
            print("用例的后置步骤有：%s" % self.teardown)
            c = Api(3, self.session, self.case_param)
            c.request()


class Api:

    def __init__(self, case_id, session, params):
        self.session = session
        self.api = self.get_api_info(case_id)
        self.params = params
        self.result = None

    def request(self):

        print("用例参数: %s" % self.params)
        body = self.api.get("c_body")
        headers = self.api.get("c_header")
        if not body:
            body = '{}'
        if not headers:
            headers = '{}'

        # url参数替换
        if '$' in self.api.get("url"):
            self.api["url"] = replace_url(self.api.get("url"), self.params)
        print("请求的url: %s" % self.api.get("url"))

        if '$' in self.api.get("c_body"):
            body = replace_url(self.api.get("c_body"), self.params)

        if '$' in self.api.get("c_header"):
            headers = replace_url(self.api.get("c_header"), self.params)

        if self.api.get("method") == "GET":
            print("发起GET请求")
            res = self.session.get(self.api.get("url"), headers=eval(headers))
        else:
            print("发起POST请求")
            res = self.session.post(self.api.get("url"), json=eval(body), headers=eval(headers))

        self.result = res

        self.save_tmp()

    def get_json(self):
        return self.result.json()

    def save_tmp(self):
        # 保存参数
        if self.api.get("c_save_param", 0):
            c_save_params = eval(self.api.get("c_save_param"))
            for i in c_save_params:
                key = i.get("name")
                print(key)
                value = save_params(self.result, i)
                print(value)
                self.params[key] = value
        else:
            return False

    def get_api_info(self, id):
        api_info = case_detail(id)
        # api_info = {
        #     "url": "https://account.teambition.com/api/login/email",
        #     "method": "POST",
        #     "body": {
        #         "email": "wenbo5@test.com",
        #         "password": "Zwb111111",
        #         "client_id": "90727510-5e9f-11e6-bf41-15ed35b6cc41",
        #         "response_type": "session",
        #         "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiI5MDcyNzUxMC01ZTlmLTExZTYtYmY0MS0xNWVkMzViNmNjNDEiLCJpYXQiOjE1ODg4NjA5MzcsImV4cCI6MTU4ODg2NDUzN30.5wMkSL975r8z21vgYW-GZUCpP0uJs3EwvJrs5LBv_V8"
        #     }
        # }
        return api_info

    def asserts(self):
        # TODO 断言类型header, code, body?
        if eval(self.api.get("c_assert")):
            res = self.result
            for k, v in eval(self.api.get("c_assert")).items():
                if res.json().get(k) == v:
                    return {"Result": 'PASS', "Response": res.content.decode('utf8')}
                else:
                    break
            return {"Reuslt": 'FAIL', "Response": res}


def replace_url(url, param):

    tmp = url.split('${')
    for i in tmp[1:]:
        for j in range(1, len(i)):
            key = i.split("}")[0]
            url = url.replace("${%s}" % key, param[key])
            break

    return url
