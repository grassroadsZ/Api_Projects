# -*-conding:utf-8
# @Time:2019-06-01 7:06
# @auther:grassroadsZ
# @file:File_path.py

import os

# 获取项目的根目录
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 将根目录下的各项目依赖目录使用join拼接起来
CASES_PATH = os.path.join(BASE_PATH, "cases")
CONFIG_PATH = os.path.join(BASE_PATH, "config")
DATAS_PATH = os.path.join(BASE_PATH, "datas")
LIBS_PATH = os.path.join(BASE_PATH, "libs")
LOGS_PATH = os.path.join(BASE_PATH, "logs")
OPTIONS_PATH = os.path.join(BASE_PATH, "options")
REPORTS_PATH = os.path.join(BASE_PATH, "reports")

# 文件路径：
# 配置文件
Config_File_Path = os.path.join(CONFIG_PATH, "case_config.conf")
User_File_Path = os.path.join(CONFIG_PATH,"user.conf")
# excel
Excel_File_Path = os.path.join(DATAS_PATH, "cases.xlsx")


if __name__ == '__main__':
    print(BASE_PATH)
    print(Config_File_Path)


