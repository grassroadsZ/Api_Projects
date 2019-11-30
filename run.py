'''
-*-conding:utf-8
@Time:2019-05-21 19:00
@auther:grassroadsZ
@file:run.py.py
'''
import unittest
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from libs import HTMLTestRunnerNew
from options.File_path import REPORTS_PATH, CASES_PATH, User_File_Path
from options.handle_user import generate_user_config

if not os.path.exists(User_File_Path):
    generate_user_config()

one_load = unittest.TestLoader()
one_suite = unittest.TestLoader.discover(one_load, start_dir=CASES_PATH, )

now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
fina = REPORTS_PATH
with open(os.path.join(fina, now + "_report" + ".html"), "wb") as file:
    test_runner = HTMLTestRunnerNew.HTMLTestRunner(
        stream=file,
        verbosity=2,
        title="测试报告",
        description="接口测试",
        tester="grassroadsZ")
    test_runner.run(one_suite)

msg = MIMEMultipart()
recevier = ['2313519547@qq.com', '1342478656@qq.com']
msg["from"] = "zys17666541106@163.com"
msg["to"] = ','.join(recevier)
msg["subject"] = u"接口测试报告"

txt = MIMEText(u"测试结果详情请看附件。", "plain", "utf-8")
msg.attach(txt)

lists = os.listdir(REPORTS_PATH)  # 获取该目录下的所有文件、文件夹，保存为列表

# 对目录下的文件按创建的时间进行排序
lists.sort(key=lambda fn: os.path.getmtime(REPORTS_PATH + "/" + fn))
# lists[-1]取到的是最新生成的文件或文件夹
print(('最新的文件是：' + lists[-1]))
file = os.path.join(REPORTS_PATH, lists[-1])

# 构造附件
att = MIMEText(open(file, "rb").read(), "base64", "utf-8")

att["Content-Type"] = "application/octet-stream"
att.add_header("Content-Disposition", 'attachment', filename=(file))
att["Accept-Language"] = "zh-CN"
att["Accept-Charset"] = "ISO-8859,utf-8"
msg.attach(att)

try:
    smtpObj = smtplib.SMTP_SSL(host='smtp.163.com')
    smtpObj.connect("smtp.163.com", "465")
    state = smtpObj.login("zys17666541106@163.com", "wangyi163com")
    if state[0] == 235:
        smtpObj.sendmail(msg["from"], msg["to"].split(','), msg.as_string())
        print(u"邮件发送成功")
except Exception as e:
    print('false',e)
