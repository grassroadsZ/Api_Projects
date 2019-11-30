"""
-*-conding: utf-8
@Time:2019-06-07 20:00
@Auther:grassroadsZ
@File:test_05_invest.py
"""

import unittest
from libs.ddt import ddt, data
from options import File_path
from options.handle_log import MyLog
from options.handle_config import HandleConfig
from options.handle_excel import ExcelOption
from options.handle_mysql import HandleMysql
from options.handle_requests import MyRequests
from options.handle_replace import DataReplace


@ddt
class TestInvest(unittest.TestCase):
    """测试充值的类"""
    exl = ExcelOption(filename=File_path.Excel_File_Path, sheetname="invest")
    case_list = exl.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.do_log = MyLog().out()
        cls.do_config = HandleConfig()
        cls.myrequest = MyRequests()
        cls.mysql = HandleMysql()
        cls.do_log.info("{:*^40s}".format("测试投资开始"))

    @classmethod
    def tearDownClass(cls):
        cls.do_log.info("{:*^40s}".format("测试投资结束"))
        cls.myrequest.close()
        cls.mysql.close()

    @data(*case_list)
    def test_invest(self, case_list):
        """
        测试投资
        :return: 当前测试用例的名称及测试结果
        """
        # do_log.info("\n测试用例名称是{}".format(inspect.stack()[0][3]))
        tittle = case_list.tittle
        result_pass = self.do_config("result", "success")
        result_fail = self.do_config("result", "Fail")

        data = DataReplace.loanId_replace(case_list.data)

        res = TestInvest.myrequest(case_list.method, self.do_config("api", "base_url") + case_list.url, data)

        try:
            self.assertEqual(200, res.status_code,
                             msg="测试【{}】失败，响应码为【{}】".format(case_list.tittle, res.status_code))
        except AssertionError as e:
            self.do_log.error("{}不通过,原因是{}\n".format(tittle,e))
            raise e

        # 如果响应信息里面有加标成功就管理员审核
        if res.json().get("msg") == "加标成功":
            check_sql = case_list.check_sql
            loan_id = self.mysql(DataReplace.loanId_replace(check_sql))["id"]
            # DataReplace.load_id = loan_id  # 创建一个类属性
            # setattr(对象，字符串的类型的属性名，设置的属性值)，与getattr连用
            setattr(DataReplace, "load_id", loan_id)

        try:
            self.assertEqual(str(case_list.expected),res.json().get("code"),msg=tittle)

        except AssertionError as a:
            self.do_log.error("{}不通过,原因是{}\n".format(tittle, a))
            self.exl.excel_write(row=case_list.case_id + 1,
                                 real_result=res.text,
                                 result=result_fail)
            raise a
        else:
            self.do_log.info("{},Pass\n".format(tittle))
            self.exl.excel_write(row=case_list.case_id + 1,
                                 real_result=res.text,
                                 result=result_pass)


if __name__ == '__main__':
    unittest.main()

