import smtplib
import os
from common.getconf import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common.getfiledir import REPORTDIR
from common.log import mylog


class Opr_email(object):

    def __init__(self):
        """
        初始化文件路径与相关配置
        """
        self.conf = Config()
        all_path = []
        for maindir, subdir, file_list in os.walk(REPORTDIR):
            pass
        for filename in file_list:
            all_path.append(os.path.join(REPORTDIR, filename))
        self.filename = all_path[0]
        self.host = self.conf.get('email', 'host')
        self.port = self.conf.get('email', 'port')
        self.user = self.conf.get('email', 'user')
        self.pwd = self.conf.get('email', 'pwd')
        self.from_addr = self.conf.get('email', 'from_addr')
        self.to_addr = self.conf.get('email', 'to_addr')

    def get_email_host_smtp(self):
        """
        连接stmp服务器
        :return:
        """
        self.smtp = smtplib.SMTP_SSL(host=self.host, port=self.port)
        self.smtp.login(user=self.user, password=self.pwd)

    def made_msg(self):
        """
        构建一封邮件
        :return:
        """
        self.msg = MIMEMultipart()

        with open(self.filename, 'rb') as f:
            content = f.read()
        # 创建文本内容
        text_msg = MIMEText(content, _subtype='html', _charset='utf8')
        # 添加到多组件的邮件中
        self.msg.attach(text_msg)
        # 创建邮件的附件
        report_file = MIMEApplication(content)
        report_file.add_header('Content-Disposition', 'attachment', filename=str.split(self.filename, '\\').pop())

        self.msg.attach(report_file)
        # 主题
        self.msg['subject'] = '自动化测试报告'
        # 发件人
        self.msg['From'] = self.from_addr
        # 收件人
        self.msg['To'] = self.to_addr

    def send_email(self):
        """
        发送邮件

        :return:
        """
        self.get_email_host_smtp()
        self.made_msg()
        self.smtp.send_message(self.msg, from_addr=self.from_addr, to_addrs=self.to_addr)
        mylog.info('\n邮件发送成功！')
        return '发送邮件成功'