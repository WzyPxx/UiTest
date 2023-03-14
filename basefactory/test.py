from selenium.webdriver.common.by import By

from basefactory.browseroperator import BrowserOperator
from basefactory.webdriverOperator import WebdriverOperator
from common.factory import Factory
from common.getcase import ReadCase

fac = Factory()

isOK, result = fac.init_execute_case()

for acases in result:
    for key, cases in acases.items():
        for case in cases:
            isOK, result = fac.execute_keyword(**case)
            print(result)
