from selenium.webdriver.common.by import By

from basefactory.browseroperator import BrowserOperator
from basefactory.webdriverOperator import WebdriverOperator
from common.factory import Factory

fac = Factory()
isOK, result = fac.init_execute_case()
print(result)
