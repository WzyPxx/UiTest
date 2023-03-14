import openpyxl  # 操作xlsx，支持读写
import os
from common.getfiledir import DATADIR  # 导入data目录

# 得到case文件的路径
file = os.path.join(DATADIR, 'case.xlsx')


# 初始化类，顺便读取一下用例文件
class ReadCase(object):
    def __init__(self):
        self.sw = openpyxl.load_workbook(file)
        # print(self.sw)

    def openxlsx(self, file):
        """
            打开文件
            :param file:
            :param dir:
            :return:
            """
        # self.sw = openpyxl.load_workbook(file)

    def readallcase(self):
        """
            取所有sheet页
            :return:list,返回sheet页里的数据
            """
        sheet_list = []
        for sh in self.sw:
            # 读取所有可执行用例时规避掉公共用例，因为公共用例是要在所有可执行用例里调用的，公共用例不能自己单独运行
            # 注意：公共用例不能调用自身,递归死循环
            if 'common' != sh.title.split('_')[0] and 'common' != sh.title.split('-')[0] and sh.title[0] != '#':
                isOK, result = self.readcase(sh)
                if isOK:
                    sheet_list.append(result)
        if sheet_list is None:
            return False, '用例集是空的，请检查用例'
        return True, sheet_list

    def readcase(self, sh):
        """
               组合sheet页的数据
               :param sh:
               :return: list,返回组合数据
            """
        # 参数传入一个sheet页对象，然后判空
        if sh is None:
            return False, '用例页参数未传'
        # 通过列表保存sheet的每一行，判空
        datas = list(sh.rows)
        if not datas:
            return False, '用例[' + sh.title + ']里面为空！'
        # 得到第一行为title
        title = [i.value for i in datas[0]]
        rows = []
        sh_dict = {}
        # 用一个循环得到每一行的用例与title结合成一个字典json串，返回
        for i in datas[1:]:
            data = [v.value for v in i]
            row = dict(zip(title, data))
            try:
                if str(row['id'])[0] != '#':
                    row['sheet'] = sh.title
                    rows.append(row)
            except KeyError:
                raise e
                rows.append(row)
            sh_dict[sh.title] = rows
        return True, sh_dict

    # 读取公共用例
    def get_common_case(self, case_name):
        """
            得到公共用例
            :param case_name:
            :return:
            """
        try:
            sh = self.sw.get_sheet_by_name(case_name)
        except KeyError:
            return False, '未找到公共用例[' + case_name + '], 请检查用例!'
        except DeprecationWarning:
            pass
        return self.readcase(sh)

