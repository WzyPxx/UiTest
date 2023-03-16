import time  # 处理等待、隐式、显示等待
import os  # 用来处理截图保存的路径
import ddddocr as ddddocr  # 识别验证码

from common.getfiledir import SCREENSHOTDIR  # 截图路径
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 前一个隐式等待的异常，后一个显示等的异常
from selenium.webdriver import Chrome  # 用来声明driver是Chrome对象，方便driver联想出来方法
from selenium.webdriver.support import expected_conditions as EC  # 判断元素的16种方法，显示等待用到
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待
from selenium.webdriver.common.by import By  # 可以By.ID，By.NAME等来用来决定元素定位,显示等待中用


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

    def web_implicitly_wait(self, **kwargs):
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
        # 里面的s是用例传过来的，调试时，只需要传指定time传一个数字，例：time = 5，每次页面刷新，程序将等待页面元素加载5秒，5
        # 秒后，不管加载成功与否都执行下一行代码，如果2秒有加载完，那么不必等5秒，直接执行下一行代码
        # 切记，隐式等待只需要初始化浏览器调用一次，后面的代码都会隐式等待。

    def web_element_wait(self, **kwargs):
        """
            显示等待
            :return:
            """
        try:
            type = kwargs['type']  # 定位类型
            locator = kwargs['locator']  # 定位参数
        except KeyError:
            return False, '未传需要等待元素的定位参数'
        # 传入时间，如果没传，默认等待30秒
        try:
            s = kwargs['time']
            if s is None:
                s = 30
        except KeyError:
            s = 30
        # 每0.5秒轮寻一次属性id为locator的元素是否可见，可见就跳出等待，返回等等元素出现成功；超过s秒便等待失败，返回元素等待出现失败，截图等信息
        try:
            if type == 'id':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.ID, locator)))
            elif type == 'name':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.NAME, locator)))
            elif type == 'class':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, locator)))
            elif type == 'xpath':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.XPATH, locator)))
            elif type == 'css':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            else:
                return False, '不能识别元素类型[' + type + ']'
        except TimeoutException:
            screenshot_path = self.get_screenshot_as_file()
            return False, '元素[' + locator + ']等待出现失败,已截图[' + screenshot_path + '].'
        return True, '元素[' + locator + ']等待出现成功'

    def element_input(self, **kwargs):
        """
            根据定位器类型定位元素输入内容
            :param kwargs:
            :return:
            """
        try:
            type = kwargs['type']  # 定位器的类型
            locator = kwargs['locator']  # 定位参数
            text = str(kwargs['input'])  # 输入内容
        except KeyError:
            return False, '缺少传参'
        try:
            index = kwargs['index']  # 元素的在List里下标
        except KeyError:
            index = 0
        # 用来查找页面元素是否存在的，如果存在，将元素找到存在elem变量，继续执行，如果失败，截图，返回False与失败日志
        isOK, result = self.find_element(type, locator, index)
        # 元素没找到，返回失败结果
        if not isOK:
            return isOK, result
        elem = result
        # 识别验证码
        if text == '验证码':
            # 获取验证码，存储为本地图片
            elems = self.driver.find_element(by=By.ID, value='chkimg')
            # 将获取的图片命名
            elems.screenshot('验证码.png')
            # 通过ddddocr包识别验证码
            ocr = ddddocr.DdddOcr(old=True)
            with open("验证码.png", 'rb') as f:
                image = f.read()
            # 将识别后的验证码4位数存储进res变量
            res = ocr.classification(image)
            text = res
        try:
            elem.send_keys(text)
        except Exception:
            screenshot_path = self.get_screenshot_as_file()
            return False, '元素[' + locator + ']输入[' + text + ']失败,已截图[' + screenshot_path + '].'
        return True, '元素[' + locator + ']输入[' + text + ']成功!'

    def find_element(self, type, locator, index=None):
        """
            定位元素
            :param type:
            :param itor:
            :param index:
            :return:
            """
        time.sleep(1)
        # isinstance(self.driver, selenium.webdriver.Chrome.)
        if index is None:
            index = 0
        type = str.lower(type)
        try:
            if type == 'id':
                elem = self.driver.find_elements(by=By.ID, value=locator)[index]
            elif type == 'name':
                elem = self.driver.find_elements(by=By.NAME, value=locator)[index]
            elif type == 'class':
                elem = self.driver.find_elements(by=By.CLASS_NAME, value=locator)[index]
            elif type == 'xpath':
                elem = self.driver.find_elements(by=By.XPATH, value=locator)[index]
            elif type == 'css':
                elem = self.driver.find_elements(by=By.CSS_SELECTOR, value=locator)[index]
            else:
                return False, '不能识别元素类型:[' + type + ']'
        except Exception as e:
            screenshot_path = self.get_screenshot_as_file()
            return False, '获取[' + type + ']元素[' + locator + ']失败,已截图[' + screenshot_path + '].'
        return True, elem

    def element_click(self, **kwargs):
        """
            点击操作
            :param kwargs:
            :return:
            """
        try:
            type = kwargs['type']  # 定位器的类型
            locator = kwargs['locator']  # 定位参数
        except KeyError:
            return False, '缺少传参'
        try:
            index = kwargs['index']  # 元素的在List里下标
        except KeyError:
            index = 0
        isOK, result = self.find_element(type, locator, index)
        if not isOK:  # 元素没找到，返回失败结果
            return isOK, result
        elem = result
        try:
            elem.click()
        except Exception:
            screenshot_path = self.get_screenshot_as_file()
            return False, '元素[' + locator + ']点击失败,已截图[' + screenshot_path + '].'
        return True, '元素[' + locator + ']点击成功'
