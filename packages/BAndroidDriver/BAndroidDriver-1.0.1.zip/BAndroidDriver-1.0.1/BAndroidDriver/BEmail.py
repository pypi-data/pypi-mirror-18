#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
 :Description:    邮件自封装类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

class BEmail(object):

    def __init__(self):
        pass

    def putemail(self,toemail,Str):
        # 第三方 SMTP 服务
        mail_host = ""  # 设置服务器
        mail_user = ""  # 用户名
        mail_pass = ""  # 口令

        sender = ''
        receivers = toemail  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        message = MIMEText(Str, 'plain', 'utf-8')
        message['From'] = Header("Interface", 'utf-8')
        message['To'] = Header("you", 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            subject = "通知"
            message['Subject'] = Header(subject, 'utf-8')
            smtpObj.sendmail(sender, receivers, message.as_string())
            print "邮件发送成功"
            # time.sleep(1)
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"
