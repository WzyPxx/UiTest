import time  # 处理等待、隐式、显示等待
import os  # 用来处理截图保存的路径
import win32con
import win32gui
from selenium.webdriver import Chrome
from selenium import webdriver  #通过html属性得到元素，进而操作元素的方法属性
from selenium.webdriver.chrome.service import Service
from common.getconf import Config
from common.getfiledir import BASEFACTORYDIR, SCREENSHOTDIR  # 截图路径
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 前一个隐式等待的异常，后一个显示等的异常
from selenium.webdriver import Chrome  # 用来声明driver是Chrome对象，方便driver联想出来方法
from selenium.webdriver.support import expected_conditions as EC  # 判断元素的16种方法，显示等待用到
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待
from selenium.webdriver.common.by import By  # 可以By.ID，By.NAME等来用来决定元素定位,显示等待中用

class BrowserOperator(object):
        def __init__(self):
            self.conf =Config()
            self.driver_path = os.path.join(BASEFACTORYDIR,'chromedriver.exe')
            self.driver_type = str(self.conf.get('base','browser_type')).lower()
        def open_url(self,**kwargs):
            """
                打开网页
                :param url:
                :return: 返回 webdriver
                """
            try:
                url = kwargs['locator']
            except KeyError:
                return False, '没有URL参数！'
            """
                判断使用那个浏览器
            """
            try:
                if self.driver_type == 'chrome':
                    # 处理chrom弹出的info
                    # chrome_options = webdriver.ChromeOptions()
                    # #option.add_argument('disable-infobars')
                    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                    # self.driver = webdriver.Chrome(options=chrome_options, executable_path=self.driver_path)
                    self.driver = webdriver.Chrome(service= Service(self.driver_path))
                    self.driver.maximize_window()
                    self.driver.get(url)
                elif self.driver_type == 'IE':
                    print('IE 浏览器')
                else:
                    print('火狐浏览器')
            except Exception as e:
                return False, e
            return True, self.driver
        def close_browser(self,**kwargs):
            """
                关闭浏览器
                :return:
                """
            time.sleep(1)
            self.driver.quit()
            time.sleep(2)
            return True, '关闭浏览器成功'
        def upload_file(self,**kwargs):
            """
                    上传文件
                    :param kwargs:
                    :return:
                    """
            try:
                dialog_class = kwargs['type']
                file_dir = kwargs['locator']
                button_name = kwargs['index']
            except KeyError:
                return False, '没传对话框的标记或没传文件路径'
            if self.driver_type == 'chrome':
                title = '打开'
            elif self.driver_type == 'IE':
                title = '文件上传'
            elif self.driver_type == 'firefox':
                title = '选择要加载的文件'
            else:
                title = ""  # 这里根据其它不同浏览器类型来修改
            # 找元素
            # 一级窗口"#32770","打开"
            dialog = win32gui.FindWindow(dialog_class,title)
            if dialog == 0:
                return False, '传入对话框的class定位器有误'
            # 向下传递
            ComboBoxEx32 = win32gui.FindWindow(dialog, 0, 'ComboBoxEx32', None)  # 二级
            ComboBox = win32gui.FindWindow(ComboBoxEx32, 0, 'ComboBox', None)  # 三级
            # 编辑按钮
            edit = win32gui.FindWindow(ComboBox, 0, 'Edit', None)  # 四级
            # 打开按钮
            button = win32gui.FindWindowEx(dialog, 0, 'Button', button_name)  # 二级
            if button == 0:
                return False, '按钮text属性传值有误'
            # 输入文件的绝对路径，点击“打开”按钮
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_dir)  # 发送文件路径
            time.sleep(1)
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
            return True, '上传文件成功'

# 需要浏览器driver对象，所以初始化这个对象为私有属性
class WebdriverOperator(object):
    def __init__(self, driver: Chrome):
        self.driver = driver

    def get_screenshot_as_file(self):
        """
            截屏保存
            :return:返回路径
            """
        # 先初始化文件路径与文件名称，文件名使用时间戳命名，保存为png
        pic_name = str.split(str(time.time()), '.')[0] + str.split(str(time.time()), '.')[1] + '.png'
        screent_path = os.path.join(SCREENSHOTDIR, pic_name)
        # 截屏代码，因为我们是截浏览器的屏，所以使用self.driver对象调用截屏方法，传入路径，它便会自动截屏保存在screent_path文件中，最后返回路径
        self.driver.get_screenshot_as_file(screent_path)
        return screent_path
    def web_implicitly_wait(self,**kwargs):
        """
            隐式等待
            :return:
            type  存时间
            """
        try:
            s = kwargs['time']
        except KeyError:
            s = 10
        try:
            self.driver.implicitly_wait(s)
        except NoSuchElementException:
            return False, '隐式等待设置失败!'
        return True, '隐式等待设置成功'
        """
            里面的s是用例传过来的，调试时，只需要传指定time传一个数字，例：time = 5，每次页面刷新，程序将等待页面元素加载5秒，5
            秒后，不管加载成功与否都执行下一行代码，如果2秒有加载完，那么不必等5秒，直接执行下一行代码
            切记，隐式等待只需要初始化浏览器调用一次，后面的代码都会隐式等待。
            """

