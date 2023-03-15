import unittest  # UT测试库
from ddt import ddt, data, unpack  # 数据驱动装饰器
from common.log import mylog  # 日志打印
from common.factory import Factory  # 框架的核心类


@ddt
class MyTesting(unittest.TestCase):
    fac = Factory()
    isOK, excu_cases = fac.init_execute_case()

    @data(*excu_cases)  # 装饰器来帮忙遍历exc_cases用例
    def test_run(self, acases):
        for key, cases in acases.items():
            mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
            print('\n')
            for case in cases:
                isOK, result = self.fac.execute_keyword(**case)
                if isOK:
                    print(result)
                    mylog.info(result)
                else:
                    mylog.error(result)
                    raise Exception(result)
            mylog.info('\n----------用例【%s】结束----------\n' % cases[0].get('sheet'))


