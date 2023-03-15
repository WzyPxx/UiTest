import logging
import os
from logging.handlers import TimedRotatingFileHandler
from common.getconf import Config
from common.getfiledir import LOGDIR


class Handlogging():

    @staticmethod
    def emplorlog():
        conf = Config()
        # set format
        formatter = logging.Formatter("%(asctime)s - %(name)s-%(levelname)s %(message)s")

        # create log set getlog level
        mylog = logging.getLogger('Weizhengyu')
        mylog.setLevel(conf.get('LOG', 'level'))

        # create outputsteam set level
        sh = logging.StreamHandler()
        sh.setLevel(conf.get('LOG', 'level'))
        sh.setFormatter(formatter)
        mylog.addHandler(sh)

        # create file set level
        # fh = logging.FileHandler(os.path.join(LOGDIR,'server.log'), encoding='utf-8')

        log_path = os.path.join(LOGDIR, 'server')
        # interval 滚动周期，
        # when="MIDNIGHT", interval=1 表示每天0点为更新点，每天生成一个文件
        # backupCount  表示日志保存个数
        fh = TimedRotatingFileHandler(
            filename=log_path, when="D", backupCount=15, encoding='utf-8'
        )
        fh.suffix = "%Y-%m-%d.log"
        fh.setLevel(conf.get('LOG', 'level'))
        fh.setFormatter(formatter)
        mylog.addHandler(fh)
        return mylog


mylog = Handlogging.emplorlog()