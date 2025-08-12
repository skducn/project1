token
$.data.access_token
0

生成报告
步骤1，将3.jmx 生成日志文件3.jtl文件
jmeter -n -t d:\51\jmeter\project\CDRD\3.jmx -l d:\51\jmeter\project\CDRD\3.jtl

步骤2: 生成html报告 3是目录
jmeter -g d:\51\jmeter\project\CDRD\3.jtl -o d:\51\jmeter\project\CDRD\3


测试步骤
1，打开 influxdb1\influxd ，influx , 
2，打开 grafana-v12.1.0\bin\grafana-server.exe  //127.0.0.1:3000
3，打开浏览器，输入测试网址：http://192.168.0.243:8083
4，浏览器中-设置 - 代理 127.0.0.1：8888
5，打开jmeter，开始录制
6，登录，操作具体内容
7，关闭录制

