# -*- coding: utf-8 -*-
import os
from DatabaseToolsNew import cxOracle
from log import LogMgr

class JobTable(object):
    '''
    工作表
    '''
    db = cxOracle()
    logmgr = LogMgr()

    def __init__(self):
        self.jobdict = dict()
        #self.jobdict['SER_IP'] = '10.67.28.8'
        self.dbtable = 'OCRWORKFILE'
        self.dbflag = 2
    
    def job_add(self, jobtmp):
        self.jobdict = jobtmp
    
    def job_del(self):
        if self.jobdict:
            self.jobdict.clear()

    def update_item(self, find_key, find_value, update_key, update_value):
        '''
        ????????????
        @find_key       ----????????
        @find_value     ----?????????
        @update_key     ----????????
        @update_value   ----????????
        '''
        self.db.update('OCRWORKFILE',find_key, find_value, update_key, update_value)
    
    def job_todb(self):
        try:
            jobsql, jobparam = self.db.getsavesql(self.dbtable, self.jobdict, self.dbflag)
            self.db.insert(jobsql, jobparam)
        except Exception as e:
            self.logmgr.error(str(e))