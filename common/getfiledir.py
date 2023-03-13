import os

# 获取本框架各目录的绝对路径
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATADIR = os.path.join(dir, 'data')
CONFDIR = os.path.join(dir, 'config')
BASEFACTORYDIR = os.path.join(dir, 'basefactory')
RESULTDIR = os.path.join(dir, 'result')
CASEDIR = os.path.join(dir, 'excutetest')
LOGDIR = os.path.join(RESULTDIR, 'log')
REPORTDIR = os.path.join(RESULTDIR, 'report')
SCREENSHOTDIR = os.path.join(RESULTDIR, 'screenshot')
