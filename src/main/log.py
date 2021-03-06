#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging, logging.handlers
import os

class LogMgr:
    def __init__(self):

        self.LOG = logging.getLogger('all')
        code_path = os.path.dirname(__file__)
        loghdlr1 = logging.handlers.TimedRotatingFileHandler(code_path + '\\' + 'log/all.log', when='D', interval=1, backupCount=3)
        loghdlr1.suffix = "%Y-%m-%d_%H-%M-%S.log"
        fmt1 = logging.Formatter("%(asctime)s|%(pathname)s 调用函数:%(funcName)s 错误代码行数:%(lineno)d 错误等级:%(levelname)-8s 信息:%(message)s", "%Y-%m-%d %H:%M:%S")
        loghdlr1.setFormatter(fmt1)
        self.LOG.addHandler(loghdlr1)
        self.LOG.setLevel(logging.INFO)


        # self.MARK = logging.getLogger('mark')
        # loghdlr2 = logging.handlers.RotatingFileHandler(markpath, "a", 0, 1)
        # fmt2 = logging.Formatter("%(message)s")
        # loghdlr2.setFormatter(fmt2)
        # self.MARK.addHandler(loghdlr2)
        # self.MARK.setLevel(logging.INFO)

    def error(self, msg):
        if self.LOG is not None:
            self.LOG.error(msg)

    def info(self, msg):
        if self.LOG is not None:
            self.LOG.info(msg)

    def debug(self, msg):
        if self.LOG is not None:
            self.LOG.debug(msg)

    # def mark(self, msg):
    #     if self.MARK is not None:
    #         self.MARK.info(msg)


def main():
    global log_mgr
    # log_mgr = LogMgr("mylog",'mymark')
    log_mgr = LogMgr()
    log_mgr.error('[mylog]This is error log')
    log_mgr.info('[mylog]This is info log')
    log_mgr.debug('[mylog]This is debug log')
    # log_mgr.mark('[mymark]This is mark log')


if __name__ == "__main__":
    main()