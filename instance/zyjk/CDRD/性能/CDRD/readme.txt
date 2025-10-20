todo 切环境
jenkins - cdrd-test - cdrd-server - 配置（构建后操作）
定位到  url: jdbc:sqlserver://192.168.0.234:1433;DatabaseName=CDRD_TEST 修改为 CDRD_PT
执行 Build with Parameters - 选择工程 origin/test_v1.2


todo token
$.data.access_token

todo 需求文档
gitlab：http://192.168.0.241/cdrd_product_doc/product_doc

todo 生成报告
步骤1，将3.jmx 生成日志文件3.jtl文件
jmeter -n -t d:\51\jmeter\project\CDRD\3.jmx -l d:\51\jmeter\project\CDRD\3.jtl

步骤2: 生成html报告 3是目录
jmeter -g d:\51\jmeter\project\CDRD\3.jtl -o d:\51\jmeter\project\CDRD\3


todo 录制测试步骤
1，打开 influxdb1\influxd ，influx , 
2，打开 grafana-v12.1.0\bin\grafana-server.exe  //127.0.0.1:3000
3，打开浏览器，输入测试网址：http://192.168.0.243:8083
4，浏览器中-设置 - 代理 127.0.0.1：8888     
chrome://settings/?search=%E4%BB%A3%E7%90%86
5，打开jmeter，开始录制
6，登录，操作具体内容
7，关闭录制
8，jmeter操作
1，添加线程组, config element - 添加 http cookie manager
	http request defaults默认请求头， http  192.168.0.243 8083
	http header manager 
		Authorization = ${token}
		Content-Type = application/json;charset=utf-8
		charset = UTF-8
2, 添加登录请求，http request , {
  "password": "041fd352cdc85bb64c260889ff9c994f511e85741444384e41807b5815499876afe3a5d1f96deaa7df941a75ff3d4b53750a634980556527daa6100942e8a7cd8e83435ba2bddb06c0ca7338577b975e5e815ec0a1c6eb97e1309e6e49e9f7d93637e527d5c21b49ab",
  "username": "${username}"
}
	json extractor 
		Names of created variables: token
		Json path expressions: $.data.access_token
		match No. : 1
2,  添加录制脚本，non-test elements - 添加 https testscript recorder
	2.1 Test Plan Creation - TestPlan>Thread Group
	2.2 Requests Filtering   .*192.168.0.243.*   (?i).*\.(bmp|css|js|gif|ico|jpe?g|png|swf|woff|woff2|wav|mp3|mp4).*
3, 开始录制，打开登陆网页


todo 打开监控startAgent
1,CDRD /ServerAgent-2.2.3
2, ./startAgent.sh



