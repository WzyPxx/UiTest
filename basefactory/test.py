from selenium.webdriver.common.by import By

from basefactory.browseroperator import BrowserOperator, WebdriverOperator

bo = BrowserOperator()
isOK, deiver = bo.open_url(locator='https://www.baidu.com')
wb = WebdriverOperator(deiver)
isOK, result = wb.web_element_wait(type='xpath', locator='//*[@id="kw"]', s=0.0001)
print(result)