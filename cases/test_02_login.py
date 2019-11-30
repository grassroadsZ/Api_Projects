# -*-conding:utf-8
# @Time:2019-05-21 22:22
# @auther:grassroadsZ
# @file:test_01_register.py

import unittest
import inspect
from libs.ddt import ddt, data
from options.handle_config import do_config
from options.handle_excel import ExcelOption
from options.handle_log import MyLog
from options import File_path
from options.handle_requests import MyRequests
from options.handle_replace import DataReplace


do_log = MyLog().out()


@ddt
class TestLogin(unittest.TestCase):
    """测试登陆的类"""
    exl = ExcelOption(filename=File_path.Excel_File_Path, sheetname="login")
    case_list = exl.get_cases()

    @classmethod
    def setUpClass(cls):
        do_log.info("{:*^40s}".format("测试登陆开始"))
        cls.myrequest = MyRequests()

    @classmethod
    def tearDownClass(cls):
        do_log.info("{:*^40s}".format("测试登陆结束"))
        cls.myrequest.close()

    @data(*case_list)
    def test_login(self, case_list):
        """
        测试注册
        :return: 当前测试用例的名称及测试结果
        """

        do_log.info("\n测试用例名称是{}".format(inspect.stack()[0][3]))

        case_num = case_list.case_id
        msg = case_list.tittle
        api = do_config("api","base_url")+case_list.url
        method = case_list.method
        except_result = case_list.expected
        response = case_list.actual
        data = DataReplace().phone_replace( case_list.data )

        try:
            response = TestLogin.myrequest(method,api, data)
            self.assertEqual(except_result, response.text, msg=msg)
        except AssertionError as a:
            do_log.error("{}不通过,原因是{}\n".format(msg, a))
            self.exl.excel_write(row=case_num + 1, real_result=response.text, result=do_config("result", "Fail"))
            raise a

        else:
            do_log.error("{},Pass\n".format(msg))
            self.exl.excel_write(row=case_num + 1, real_result=response.text, result=do_config("result", "success"))


if __name__ == '__main__':
    unittest.main()
