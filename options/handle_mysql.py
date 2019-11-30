# -*-conding:utf-8
# @Time:2019-05-30 20:26
# @auther:grassroadsZ
# @file:handle_mysql.py


import random
import pymysql
import string
from options.handle_config import HandleConfig


class HandleMysql:
    """
    我的mysql处理类
    """
    def __init__(self):
        do_config = HandleConfig()
        self.connt = pymysql.connect(
            host = do_config("mysql", "host"),
            port = do_config("mysql", "port"),
            db = do_config("mysql", "db"),
            user = do_config("mysql", "username"),
            password = do_config("mysql", "test"),
            charset = "utf8",
            cursorclass = pymysql.cursors.DictCursor)
        # 创建游标
        self.cursor = self.connt.cursor()

    def __call__(self, sql, args=None, is_more=False):
        """
        执行sql并返回结果
        :param sql:需要执行的sql
        :param args:需要替换占位符%s所在的参数
        :param is_more:True/False ,默认为False只获取一条
        :return:
        """
        # 执行sql语句
        self.cursor.execute(sql, args)
        # 手动提交
        self.connt.commit()
        if is_more:
            result = self.cursor.fetchall()
        else:
            result = self.cursor.fetchone()
        return result

    @staticmethod
    def create_mobile():
        """
        生成随机手机号
        :return:生成的手机号
        """
        num_list = [133 , 149 , 153 , 173 , 177 , 180 , 181 , 189 , 191 , 199 , 130 , 131 , 132 , 145 , 155 , 156 ,
                    166 , 171 , 175 , 176 , 185 , 186 , 134 , 135 , 136 , 137 , 138 , 139 , 147 , 150 , 151 , 152 , 157 , 158 , 159 ,
                    172 , 178 , 182 , 183 , 184 , 187 , 188]
        # 使用random.chioce从序列类型随机选一个元素
        first_num = random.choice(num_list)
        # 使用（string.digits, 次数）返回一个序列类型后拼接成字符串
        second_num = "".join(random.sample(string.digits,8))
        return str(first_num) + second_num

    def is_existed_mobile(self,mobile):
        """
        判断手机号是否存在于数据库中
        :param mobile: 待判断的手机字符串类似
        :return: True/False
        """
        sql = "SELECT t.MobilePhone from member t where t.MobilePhone = %s;"
        if self(sql, args=(mobile,)):
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """
        生成数据库中不存在的手机号
        :return:
        """
        while True:
            mobile = self.create_mobile()
            if not self.is_existed_mobile(mobile):
                break
        return mobile

    def close(self):
        self.cursor.close()
        self.connt.close()


do_mysql = HandleMysql()


if __name__ == '__main__':
    # sql_1 = "SELECT * from member LIMIT 10;"
    mysql = HandleMysql()
    print( mysql.create_not_existed_mobile() )
