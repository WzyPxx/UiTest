from selenium.webdriver.common.by import By

from basefactory.browseroperator import BrowserOperator
from basefactory.webdriverOperator import WebdriverOperator
from common.factory import Factory

bo = BrowserOperator()
isOK, deiver = bo.open_url(locator='https://www.baidu.com')
wb = WebdriverOperator(deiver)
isOK, result = wb.web_element_wait(type='xpath', locator='//*[@id="kw"]', s=0.001)
print(result)
isOK, result = wb.element_input(type='xpath', locator='//*[@id="kw"]', input='飞人', index=0)
print(result)
isOK, result = wb.element_click(type='xpath', locator='//*[@id="su"]', index=0)    # 元素点击方法
print(result)
fac = Factory()
isOK, result = fac.init_execute_case()
print(result)
