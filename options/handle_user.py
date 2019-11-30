# -*-conding:utf-8
# @Time:2019-06-04 20:26
# @auther:grassroadsZ
# @file:handle_user.py

from options.handle_mysql import HandleMysql
from options.handle_requests import MyRequests
from options.handle_config import HandleConfig
from options.File_path import User_File_Path

do_config = HandleConfig()


def create_user(regname, pwd="123456"):
    """
    创建用户
    :param regname:用户名
    :param pwd:密码
    :return:键为用户名，值为信息的嵌套字典
    """
    requets = MyRequests()
    mysql = HandleMysql()
    url = do_config("api", "base_url") + "/member/register"
    while True:
        mobile = mysql.create_mobile()
        data = {"mobilephone": mobile, "pwd": pwd, "regname": regname}
        requets("post", url, data)
        sql = "SELECT t.Id from member t where MobilePhone = %s;"
        Id = mysql(sql, args=(mobile,))
        if Id:
            user_id = Id["Id"]
            break

    data_dict = {
        regname:
            {"Id": user_id,
             "regname": regname,
             "mobile": mobile,
             "pwd": pwd}}
    mysql.close()
    return data_dict


def generate_user_config():
    """
    生成三个嵌套data_dict的字典
    :return:
    """
    user_dict = {}

    tou_zi = create_user("tou_zi")
    admin = create_user("admin")
    jie_money = create_user("jie_money")

    user_dict.update(tou_zi)
    user_dict.update(admin)
    user_dict.update(jie_money)

    do_config.config_write(data=user_dict, filename=User_File_Path)
    return user_dict


if __name__ == '__main__':
    # HandleConfig().config_write( data=generate_user_config() , filename= "user.conf" )
    generate_user_config()
