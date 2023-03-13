import os  # 获取一些工程里的绝对路径
from configparser import ConfigParser
from common.getfiledir import CONFDIR


class Config(ConfigParser):
    def __init__(self):
        self.conf_name = os.path.join(CONFDIR, 'base.ini')
        super().__init__()
        super().read(self.conf_name, encoding='utf-8')

    def save_date(self, section, option, value):
        super().set(section=section, option=option, value=value)
        super().write(fp=open(self.conf_name, 'w'))
