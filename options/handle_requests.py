# -*-conding:utf-8
# @Time:2019-05-30 6:23
# @auther:grassroadsZ
# @file:handle_requests.py


import json
import requests
from options.handle_config import do_config


class MyRequests:
    """
    对request请求进行封装
    """

    def __init__(self):
        """"创建请求会话"""
        self.my_session = requests.Session()

    def __call__(self, methmod, url, data=None, is_json=False, **kwargs):
        methmod = methmod.lower()
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                print(e)
                data = eval(data)

        if methmod == "get":
            res = self.my_session.request(methmod, url, params=data, **kwargs)
        elif methmod == "post":
            if is_json:
                res = self.my_session.request(methmod, url, json=data, **kwargs)
            else:
                res = self.my_session.request(methmod, url, data=data, **kwargs)
        else:
            res = None
            print("不支持{}的请求方法".format(methmod))
        return res

    def close(self):
        return self.my_session.close()

do_request = MyRequests()


if __name__ == '__main__':
    # 注册
    # url_1 = do_config("api", "base_url") + "/member/register"
    # data1 = {"mobilephone": "13666661661", "pwd": "123456"}
    data1 = '{"mobilephone": "18962705941", "pwd":123456}'
    # 登陆
    login_url = do_config("api", "base_url") + "/member/login"
    # 充值
    recharge_url = do_config("api", "base_url") + "/member/recharge"
    recharge_data = {"mobilephone": "18962705941", "amount": 2345}
    requests = MyRequests()
    # res_1 = requests("post", url = url_1, data = data1)
    res_2 = requests("post", url = login_url, data = data1)
    res_3 = requests("post", url = recharge_url, data = recharge_data)
    # print(res_1.text)
    print(res_2.text)
    print(res_3.text)
