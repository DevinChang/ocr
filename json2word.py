#-*-coding:utf-8-*-
import os
from log import LogMgr
#savapath 为存入文件夹
#savename 为存入名字不包含后缀
def json2word(wordlist,savepath,savename):# savepath = './word' # savename = 'test1'
    emb_filename = os.path.join(savepath, savename+'.doc')
    if not os.path.isdir(os.path.split(emb_filename)[0]):
        os.makedirs(os.path.split(emb_filename)[0])
    try:
        with open(emb_filename, "w",encoding='utf-8') as f:
            for i in wordlist:
                f.write(i + "\n")
            f.close()
    except Exception as e:
        print(e)
        log_mgr = LogMgr()
        log_mgr.error('[mylog]This is error log')


# savepath = './word'
# savename = 'test1'
# wordlist = ["淋日期有合","【有效期】24个月","请仔细阅读说明书井在医师指导下使用"]
# json2word(wordlist,savepath,savename)