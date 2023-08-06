# coding=utf-8
import os

import yagmail


def send_mail(to, subject, content, attachments=None,
              username=None, password=None, host=None, port='587'):
    """
    发送邮件
    :param to:              邮件接收者, 支持列表、字典
    :param subject:         邮件主题
    :param content:         邮件正文
    :param attachments:     邮件附件的路径, 列表
    :param username:        发件者邮箱(默认从环境变量 MAIL_USERNAME 中获取)
    :param password:        发件者密码(默认从环境变量 MAIL_PASSWORD 中获取)
    :param host:            发件者服务器地址(默认从环境变量 MAIL_HOST 中获取)
    :param port:            发件者服务器端口(默认 587)
    :return:
    """
    if not username:
        username = os.environ.get('MAIL_USERNAME')

    if not password:
        password = os.environ.get('MAIL_PASSWORD')

    if not host:
        host = os.environ.get('MAIL_HOST')

    if not (username and password and host):
        raise AttributeError('Username/Password/Host is necessary to send mail.')

    with yagmail.SMTP(user=username, password=password, host=host, port=port) as yag:
        yag.send(to=to, subject=subject, contents=content, attachments=attachments)


def render_template(temp, **kwargs):
    """
    根据简易模板生成邮件正文.
    做简单的替换: {{ some_key }} => value_of_key

    :param temp:    模板文件或模板内容
    :param kwargs:  需要替换的关键字
    :return:        由模板生成的内容
    """
    if os.path.exists(temp):
        with open(temp) as fp:
            template = fp.read()
    else:
        template = temp

    for k, v in kwargs.iteritems():
        template = template.replace('{{ %s }}' % k, v)

    return template
