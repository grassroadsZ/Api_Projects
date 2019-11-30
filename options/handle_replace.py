"""
-*-conding: utf-8
@Time:2019-06-06 6:27
@Auther:grassroadsZ
@File:handle_replace.py
"""
import re
from options.handle_config import HandleConfig
from options.handle_mysql import HandleMysql
from options.File_path import User_File_Path


class DataReplace:
    """
    实现参数化替换
    """
    not_existed_phone = re.compile(r"\$\{mobile\}")
    existed_phone = re.compile(r"\$\{exist_phone\}")
    touzi_phone = re.compile(r"\$\{touzi_phone\}")
    admin = re.compile(r"\$\{admin\}")
    jie_money_id = re.compile(r"\$\{jie_money_id\}")
    loadId = re.compile(r"\$\{project_id\}")

    do_mysql = HandleMysql()

    @classmethod
    def not_existed_phone_replace(cls, data):
        """
        参数化替换为不存在的手机号
        :param data:
        :return:参数化替换数据库中不存在的手机号
        """
        if re.search(cls.not_existed_phone, data):
            data = re.sub(cls.not_existed_phone, cls.do_mysql.create_not_existed_mobile(), data)
        return data

    @classmethod
    def existed_phone_replace(cls, data):
        """
        参数化替换为不存在的手机号
        :param data:
        :return:替换从用户配置表中获取的已存在的手机号
        """
        do_config = HandleConfig(filename=User_File_Path)
        if re.search(cls.existed_phone, data):
            data = re.sub(
                cls.existed_phone, str(do_config("admin", "mobile")), data)
        return data

    @classmethod
    def touzi_phone_replace(cls, data):
        """
        参数化替换为投资人的手机号
        :param data:
        :return:替换从用户配置表中获取的投资人的的手机号
        """
        do_config = HandleConfig(filename=User_File_Path)
        if re.search(cls.touzi_phone, data):
            data = re.sub(cls.touzi_phone, str(do_config("tou_zi", "mobile")), data)
        return data

    @classmethod
    def add_testcase_replace(cls, data):
        """
        参数化替换管理员的的手机号和借款人的id
        :param data:
        :return:替换从用户配置表中获取的管理员的的手机号和借款人的id
        """
        do_config = HandleConfig(filename=User_File_Path)

        if re.search(cls.admin, data):
            data = re.sub(cls.admin, str(do_config("admin", "mobile")), data)

        if re.search(cls.jie_money_id,data):
            data = re.sub(cls.jie_money_id, str(do_config("jie_money", "id")), data)

        return data

    @classmethod
    def loanId_replace(cls, data):
        """
        参数化替换为投资人的手机号
        :param data:
        :return:替换从用户配置表中获取的已存在的手机号
        """
        do_config = HandleConfig(filename=User_File_Path)

        if re.search(cls.admin, data):
            data = re.sub(cls.admin, str(do_config("admin", "mobile")), data)

        if re.search(cls.jie_money_id,data):
            data = re.sub(cls.jie_money_id, str(do_config("jie_money", "id")), data)

        if re.search(cls.touzi_phone, data):
            data = re.sub(cls.touzi_phone, str(do_config("tou_zi", "mobile")), data)

        if re.search(cls.loadId, data):
            # 第一个参数为对象，第二个参数为字符串的属性名
            # 作用：获取这个对象(类)的实例属性值
            loadId = getattr(cls,"load_id")
            # load_id = cls.load_id
            data = re.sub(cls.loadId, str(loadId), data)

        return data



    @staticmethod
    def phone_replace(data):

        data = DataReplace.not_existed_phone_replace(data)
        data = DataReplace.existed_phone_replace(data)
        data = DataReplace.touzi_phone_replace(data)
        data = DataReplace.add_testcase_replace(data)
        # data = DataReplace.loanId_replace(data)

        return data



if __name__ == '__main__':
    not_existed = '{"mobilephone": "${mobile}", "pwd":"123456", "regname": "KeYou"}'
    exited = '{"mobilephone": "${exist_phone}", "pwd":"123456"}'
    touzi = '{"mobilephone": "${touzi_phone}", "pwd":"123456"}'
    add = '{"mobilephone": "${admin}", "pwd":"${project_id}"}'
    # print(DataReplace.not_existed_phone_replace(not_existed))
    # print(DataReplace.existed_phone_replace(exited))
    # print( DataReplace().phone_replace( not_existed ) )
    # print( DataReplace().phone_replace(exited))
    # print(DataReplace().phone_replace(touzi))





