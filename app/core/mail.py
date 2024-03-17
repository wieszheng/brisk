# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : mail.py
@Time     : 2024/3/17 0:16
@Author   : wiesZheng
@Function :
"""
import asyncio
import json
import os
import base64
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from jinja2 import Template

from config import ROOT


def get_config():
    try:
        file_path = os.path.join(ROOT, "config.json")
        if not os.path.exists(file_path):
            raise Exception("没有找的配置文件，请假查")
        with open(file_path, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"获取系统设置失败，{e}")


def render_html(filepath, **kwargs):
    with open(filepath, encoding="utf-8") as f:
        html_str = Template(f.read())
        return html_str.render(**kwargs)


async def send_mail(
        subject: str,
        content_msg: str,
        *recipient):
    data = get_config().get("email")
    from_addr = data.get("from_addr")
    smtp_server = data.get("smtp_server")
    password = data.get("password")
    # nickname base64
    original_str = "Brisk机器人"
    encoded_bytes = original_str.encode('utf-8')
    base64_encoded_str = base64.b64encode(encoded_bytes)

    # 设置总的邮件体对象，对象类型为mixed
    msg = MIMEMultipart("mixed")
    msg["From"] = Header(f'"=?UTF-8?B?{base64_encoded_str.decode("utf-8")}?=" <{from_addr}>')
    msg["To"] = Header("其他同学")
    msg["Subject"] = Header(subject, "utf-8")
    # 邮件正文内容
    msg.attach(MIMEText(content_msg, "html", "utf-8"))

    try:
        server = aiosmtplib.SMTP(
            hostname=smtp_server,
            port=465,
            use_tls=True)
        await server.connect()
        await server.login(from_addr, password)
        await server.sendmail(from_addr, [from_addr, *recipient], msg.as_string())
        await server.quit()
    except Exception as e:
        raise Exception(f"发送测试报告邮件失败：{e}")


if __name__ == '__main__':
    html = render_html(filepath=os.path.join(ROOT, "templates", "report.html"),
                       plan_name="小米",
                       env="流浪地球",
                       plan_result="成功",
                       total="123",
                       executor="wieszheng",
                       start_time="2013-01-01T00:00:00",
                       cost="43512",
                       success="112",
                       failed="10",
                       error="1",
                       skip="0")
    email_list = ["3248401072@qq.com"]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_mail("【流浪地球】测试计划【wieszheng】执行完毕",
                                      html,
                                      email_list
                                      ))
