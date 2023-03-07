from selenium import webdriver  #通过html属性得到元素，进而操作元素的方法属性
from common.getconf import Config
import os

from common.getfiledir import BASEFACTORYDIR


class BrowserOperator(object):
        def __init__(self):
            self.conf =Config()
            self.driver_path = os.path.join(BASEFACTORYDIR,'chromedriver.exe')
            self.driver_type = str(os.path.join('base','browser_type')).lower()
        
