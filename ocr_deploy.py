# -*- coding: utf-8 -*-

from ocr import MyOcr



class DeployOcr(MyOcr):
    def __init__(self):
        MyOcr.__init__(self)


    

    def _ocr_deploy(self, rec_dict):
        files = rec_dict['files']

        #ocr所需的参数
        options = {}
        options["detect_direction"] = "true" 
        options["detect_language"] = "true"
        options["probability"] = "true"
        
        #dirlist = os.listdir(imgpath)
        root = imgpath
        #dirlist, root = self._list_custom(imgpath)
        for file in files:
            if re.search(r'进口注册证|GMP|说明书|药品再注册批件|营业执照|生产许可证|进口药品许可证', file['type']):
                for img in file['img']:
                    print('Current img: {}'.format(file['img']['imgpath']))
                    try:
                        data = self.client.accurate(img['imgbase64'], options)
                    except Exception as e:
                        print('Error: ', e)
                        self.log(file['img']['imgpath'] + "Error! : " str(e))
                        continue
                    img.update({"imgjson" : data})
        
            
        for file in os.walk(imgpath):
            for file_name in file[2]:
                if re.search(r'进口注册证|GMP|说明书|药品再注册批件|营业执照|生产许可证|进口药品许可证', file_name):
                    if '备案' in file_name:
                        continue
                    if os.path.isdir(file[0] + '\\' + file_name):
                        continue
                    if not re.match(r'[jJ][pP][gG]', file_name[-3:]):
                        continue
                    datafilepath = self.datapath + file[0].split('IMG')[1]
                    if not os.path.exists(datafilepath):
                        os.makedirs(datafilepath)
                    img = self._get_file_content(file[0] + '\\' + file_name)
                    if file_name[:-4].find('.'):
                        file_name = file_name[:-4].replace('.', '') + file_name[-4:]
                    try:
                        prefix,suffix = file_name.split('.')
                    except Exception as e:
                        print('split error: {}\ncurrent file: {}'.format(e, file[0] + '\\' + file_name))
                        self.log.error(file[0] + '\\' + file_name + " Error!! : " + str(e))
                        continue
                    #判断文件是否存在
                    if os.path.isfile((datafilepath +'\{}.json').format(prefix + '_' + suffix)):
                        continue
                    print('Current img: {}'.format(file[0] + '\\' + file_name))
                    try: 
                        if self.typeid == 1:
                            data = self.client.basicGeneral(img, options)
                        elif self.typeid == 2:
                            data = self.client.general(img, options)
                        elif self.typeid == 3:
                            data = self.client.basicAccurate(img, options)
                        elif self.typeid == 4:
                            data = self.client.accurate(img, options)
                    except Exception as e:
                        print('Error: ', e)
                        self.log.error(file[0] + '\\' + file_name + " Error!! : " + str(e))
                        continue
                    self._write_json_file((datafilepath +'\{}.json').format(prefix + '_' + suffix), data)   
        
        #self._ocr()