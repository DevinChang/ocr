Requiers
	version: python3.x
	pakege:baidu_aip sdk
Use
	修改config.py中各个字段的数值即可
	@@@
	APP_ID = ***
	API_KEY = ***
	SECRET_KEY = ***
	@@@
	这些字段是通过访问https://console.bce.baidu.com/ai创建文字识别后得到的。
**=====================================================**
	""" 带参数调用通用文字识别, 图片参数为本地图片 """
client.basicGeneral(image, options)

url = "https//www.x.com/sample.jpg"

""" 调用通用文字识别, 图片参数为远程url图片 """
client.basicGeneralUrl(url);

""" 调用通用文字识别（含位置高精度版） """
client.accurate(image);

""" 调用通用文字识别（含位置信息版）, 图片参数为本地图片 """
client.general(image);

""" 调用通用文字识别（高精度版） """
client.basicAccurate(image);