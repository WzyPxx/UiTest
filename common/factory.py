from common.getconf import Config  # 配置文件读取
from common.getcase import ReadCase  # 初始化用例
from basefactory.browseroperator import BrowserOperator
from basefactory.webdriverOperator import WebdriverOperator  # 执行用例


# 初始化工厂类
class Factory(object):
    def __init__(self):
        # 配置项Function初始化进来 初始化一下两个基础类对象，因为WebdriverOperator类要在打开URL后才能初始化，先初始化为None
        self.con = Config()
        self.con_fun = dict(self.con.items('Function'))
        """
        浏览器操作对象
        """
        self.browser_opr = BrowserOperator()
        """
        网页操作对象
        """
        self.webdriver_opr = None

    def init_webdriver_opr(self, driver):
        self.webdriver_opr = WebdriverOperator(driver)

    # 初始化执行用例
    def init_execute_case(self):
        print("----------初始化用例----------")
        xlsx = ReadCase()
        isOK, result = xlsx.readallcase()
        if not isOK:
            print(result)
            print("----------结束执行----------")
            exit()
        all_cases = result
        excu_cases = []
        for cases_dict in all_cases:
            for key, cases in cases_dict.items():
                isOK, result = self.init_common_case(cases)
                if isOK:
                    cases_dict[key] = result
                else:
                    cases_dict[key] = cases
                excu_cases.append(cases_dict)
                print("----------初始化用例完成----------")
        return excu_cases

    # 初始化公共用例
    def init_common_case(self, cases):
        """
            :param kwargs:
            :return:
            """
        cases_len = len(cases)
        index = 0
        for case in cases:
            if case['keyword'] == '调用用例':
                xlsx = ReadCase()
                try:
                    case_name = case['locator']
                except KeyError:
                    return False, '调用用例没提供用例名，请检查用例'
                isOK, result = xlsx.get_common_case(case_name)
                if isOK and type([]) == type(result):
                    isOK, result_1 = self.init_common_case(result)  # 递归检查公共用例里是否存在调用用例
                elif not isOK:
                    return isOK, result
                list_rows = result[case_name]
                cases[index: index+1] = list_rows  # 将公共用例插入到执行用例中去
            index += 1
        if cases_len == index:
            return False, ''
        return True, cases


