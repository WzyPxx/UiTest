import os  # 处理路径
import unittest  # Loadcase的代码文件
from library.HTMLTestRunnerNew import HTMLTestRunner  # 执行用例，输出报告
from common.getfiledir import CASEDIR, REPORTDIR


class Test_run(object):
    # 初始化用例，与报告对象
    def __init__(self):
        self.suit = unittest.TestSuite()
        self.load = unittest.TestLoader()
        self.suit.addTest(self.load.discover(CASEDIR))
        self.runner = HTMLTestRunner(
            stream=open(os.path.join(REPORTDIR, 'report.html'), 'wb'),
            title='BOS3.0测试',
            description='测试用例执行情况',
            tester='位正雨'
        )

    def excute(self):
        self.runner.run(self.suit)


if __name__ == "__main__":
    test_run = Test_run()
    test_run.excute()