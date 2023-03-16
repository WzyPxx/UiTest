from common.getconf import Config  # 配置文件读取
from common.getcase import ReadCase  # 初始化用例
from basefactory.browseroperator import BrowserOperator
from basefactory.webdriverOperator import WebdriverOperator  # 执行用例
from common.emailUtil import Opr_email


# 初始化工厂类
class Factory(object):
    def __init__(self):
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
        self.email_opr = Opr_email()
    def init_webdriver_opr(self, driver):
        self.webdriver_opr = WebdriverOperator(driver)

    def init_execute_case(self):
        """
        初始化执行用例
        :return:
        """
        print("----------初始化执行用例----------")
        xlsx = ReadCase()  # 读取了excel里所有可执行用例
        isOK, result = xlsx.readallcase()
        if not isOK:
            print(result)
            print("----------结束执行----------")
            exit()
        all_cases = result
        exc_cases = []
        for cases_dict in all_cases:
            for key, cases in cases_dict.items():
                isOK, result = self.init_common_case(cases)  # 调用初始化公共用例
                if isOK:
                    cases_dict[key] = result
                else:
                    cases_dict[key] = cases
                exc_cases.append(cases_dict)
                print("----------初始化用例完成----------")
        return isOK, exc_cases

    def init_common_case(self, cases):
        """
        初始化公共用例
        :param cases:
        :param kwargs:
        :return:
        """
        cases_len = len(cases)
        index = 0
        for case in cases:
            if case['keyword'] == '调用用例':  # 判断是否有‘调用用例’命令，有则取公共用例合并成可执行用例
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
                cases[index: index + 1] = list_rows  # 将公共用例插入到执行用例中去
            index += 1
        if cases_len == index:
            return False, ''
        return True, cases

    def get_base_function(self, function_name):
        """
        获取执行方法
        :param function_name:
        :return:
        """
        # 传入方法名称function_name，通过getattr得到基础类的方法，成功得到方法，返回True，function，没有得到，返回False
        try:
            function = getattr(self.browser_opr, function_name)
        except Exception:
            try:
                function = getattr(self.webdriver_opr, function_name)
            except Exception:
                try:
                    function = getattr(self.email_opr, function_name)
                except Exception:
                    return False, '未找到注册方法[' + function_name + ']所对应的执行函数，请检查配置文件'
        return True, function

    def execute_keyword(self, **kwargs):
        """
        工厂函数，用例执行方法的入口
        :param kwargs:
        :return:
        """
        # 先得到用例里的keyword，然后获取到两个基础类里方法，再传入**kwargs调用，执行操作
        # 取到keyword关键字，回顾上面用例excel里的有一个keyword的字段，传入进来，先取这个字段
        try:
            keyword = kwargs['keyword']
            if keyword is None:
                return False, '没有keyword,请检查用例!'
        except KeyError:
            return False, '没有keyword,请检查用例!'
        _isbrowser = False
        # 在self.con_fun键值对里取到keyword对应的方法名
        try:
            function = self.con_fun[keyword]
        except KeyError:
            return False, '方法Key[' + keyword + ']未注册，请检查用例!'
        # 通过get_base_function得到基础类的方法
        isOK, result = self.get_base_function(function)
        if isOK:
            function = result
        else:
            return isOK, result
        # 执行基础方法，如打网点页、点击、定位、隐式等待 等
        isOK, result = function(**kwargs)

        # 如果是打开网页，是浏览器初始化，需要将返回值传递给另一个基础类
        if '打开网页' == keyword and isOK:
            url = kwargs['locator']
            self.init_webdriver_opr(result)
            return isOK, '网页[' + url + ']打开成功'
        return isOK, result


