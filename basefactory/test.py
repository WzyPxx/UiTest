from selenium.webdriver.common.by import By

from basefactory.browseroperator import BrowserOperator, WebdriverOperator

bo = BrowserOperator()
isOK, deiver = bo.open_url(locator='https://www.baidu.com')
wb = WebdriverOperator(deiver)
isOK, result = wb.web_implicitly_wait(time=0)    # 设置隐式等待，打印隐式等待的结果
print(result)
deiver.find_elements(by=By.XPATH, value='//*[@id="kw"]')[0].send_keys('飞人')
deiver.find_elements(by=By.XPATH, value='//*[@id="su"]')[0].click()
bo.close_browser()