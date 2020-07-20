import json


def replace_header(header, param):

    tmp = header.split("${")
    for i in tmp[1:]:
        for j in range(1, len(i)):
            key = i.split("}")[0]
            header = header.replace("${%s}" % key, param[key])
            break

    return eval(header)


def save_params(res, params):
    """
    保存参数
    :param res: 响应
    :param params: {}; type: 获取参数的地方，响应体，响应头，状态码
    :return:
    """
    try:
        print(params)
        type = params.get('type')
        if type == 'status_code':
            return res.status_code
        if type == 'headers':
            key = params.get('key')
            return res.headers.get(key)
        if type == 'body':
            """
            :type body
            :json 通过json来得到参数 $.data或者$.data.value[1].id
            :re 通过正则来得到参数值
            """
            if params.get('json'):
                res = res.json()
                json_path = params.get('json')
                l = json_path.split('.')  # $ data value[1] id
                # print(l)
                # print(l)
                for i in l:
                    # print(i)
                    if i == '$':
                        continue
                    if '[' in i:
                        index = i.split('[')[1][0]
                        if '$' in i:
                            res = res[int(index)]
                        else:
                            key = i.split('[')[0]
                            res = res.get(key)[int(index)]
                    else:
                        res = res.get(i)
            else:
                # 正则处理
                pass
            return res
    except Exception as e:
        return None


if __name__ == '__main__':

    header = '{ "Content-Type": "application/json", "X-Tanent-id": ${org_id}, "org": "${id}"}'
    param = {
        "org_id": "111",
        "id": "adb"
    }
    res = [{"id": 1},{"id": 2}]
    params = {
        "type": "body",
        "json": "$[1].id"
    }
    # replace_header(header, param)
    save_params(res, params)