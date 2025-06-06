# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 文件对象层 (获取路径、目录和文件信息、操作文件、系统级别)
# os.path.expanduser(path)  #把path中包含的"~"和"~user"转换成用户目录
# os.path.getatime(path)  #返回最后一次进入此path的时间。
# os.path.getmtime(path)  #返回在此path下最后一次修改的时间。
# os.path.getctime(path)  #返回path的大小
# os.path.islink(path)  #判断路径是否为链接
# os.path.ismount(path)  #判断路径是否为挂载点（）
# os.path.normcase(path)  #转换path的大小写和斜杠
# os.path.normpath(path)  #规范path字符串形式
# os.path.realpath(path)  #返回path的真实路径
# os.path.relpath(path[, start])  #从start开始计算相对路径
# os.path.samefile(path1, path2)  #判断目录或文件是否相同
# os.path.sameopenfile(fp1, fp2)  #判断fp1和fp2是否指向同一文件
# os.path.samestat(stat1, stat2)  #判断stat tuple stat1和stat2是否指向同一个文件
# os.path.splitunc(path)  #把路径分割为加载点与文件
# os.path.supports_unicode_filenames  #设置是否支持unicode路径名

# 使用Path类处理文件路径。
# 　　from pathlib import Path
# 　　# 创建一个目录
# 　　directory = Path('test_directory')
# 　　directory.mkdir(exist_ok=True)
# 　　# 创建一个文件
# 　　file_path = directory / 'example.txt'
# 　　file_path.touch()
# 　　# 读取文件内容
# 　　with file_path.open('r') as file:
# 　　    content = file.read()
# 　　    print(content)
# 　　# 删除文件和目录
# 　　file_path.unlink()
# 　　directory.rmdir()
# *********************************************************************
"""
todo 1,路径
获取当前路径 os.getcwd()
切换路径 os.chdir()
获取当前路径的父目录 os.path.abspath("..")

todo 2,判断true/false
判断是否绝对路径 os.path.isabs()
判断路径或文件是否存在 os.path.exists()
判断目录是否存在 os.path.isdir()
判断文件是否存在 os.path.isfile()
判断文件是否存在 os.access("d:\\a.jpg", os.F_OK)
判断文件是否可读 os.access("d:\\a.jpg", os.R_OK)
判断文件是否可以写入 os.access("d:\\a.jpg", os.W_OK)
判断文件是否可以执行 os.access("d:\\a.jpg", os.X_OK)

todo 3.新建/删除/重命名/分割
新建目录 os.mkdir()
新建多级目录 os.makedirs()
删除空目录 os.rmdir()
递归删除所有空目录 os.removedirs()
强制删除目录 shutil.rmtree(varFolder)
删除文件 os.remove()
创建空文件(未成功)
重命名文件或目录 os.rename()
修改文件权限和时间戳 os.chmod(file)
分割文件名和扩展名(不校验正确性) os.path.splitext()
分割路径和文件名(不校验正确性) os.path.split()

todo 4,获取目录与文件
获取目录下的所有子目录 ['/Users/linghuchong/Downloads/51/Python/project/SQL/test']
def getSubFolder(varPath):
    l_sub = []
    for entry in os.listdir(varPath):
        s_varPath_file = os.path.join(varPath, entry)
        if os.path.isdir(s_varPath_file):
            l_sub.append(s_varPath_file)
            l_sub.extend(getSubFolder(s_varPath_file))  # 递归调用,不能写在class中
    return l_sub
获取所有子目录名、文件及隐藏文件 os.listdir()
获取当前目录下所有文件/获取带路径目录下所有文件 glob.glob("*.*") / glob.glob("/Users/linghuchong/*.*")
遍历目录及子目录下文件 os.walk()
连接目录与文件名(不验证正确性) os.path.join(os.getcwd(), "ddd")
获取文件名 os.path.basename()
获取文件类型 mimetypes.guess_type()
获取文件大小 os.path.getsize()
获取文件属性 os.stat()
获取文件最后修改日期和时间 datetime.fromtimestamp(os.path.getmtime("1.jpg"))  # 将修改时间转换为日期格式


todo 5,系统级
获取系统平台 os.name()
获取环境变量 os.environ.keys()
添加路径到系统环境变量 sys.path.append()

根据环境变量的值替换 os.path.expandvars(path)，根据环境变量的值替换path中包含的”$name”和”${name}”
# os.environ['testPATH'] = 'D:/thunder'
# path = '$testPATH/train/13.png'
# print(os.path.expandvars(path))  # D:/thunder/train/13.png

"""

import os, shutil, glob, sys, pathlib, mimetypes

# todo 路径
# print("获取当前路径".center(100, "-"))
# print(os.getcwd())  # /Users/linghuchong/Downloads/51/Python/project/PO
# print(os.path.abspath("."))  # /Users/linghuchong/Downloads/51/Python/project/PO
# print(os.path.abspath(os.curdir))  # /Users/linghuchong/Downloads/51/Python/project/PO   //返回当前目录（.）
# print(os.path.dirname(__file__))  # /Users/linghuchong/Downloads/51/Python/project/PO
#
# print("切换路径".center(100, "-"))
# os.chdir("../")   # /Users/linghuchong/Downloads/51/Python/project
# os.chdir("../")   # /Users/linghuchong/Downloads/51/Python
# print(os.getcwd())
#
# print("获取当前路径的父目录".center(100, "-"))
# print(os.path.abspath(".."))  # /Users/linghuchong/Downloads/51
#
# print("获取当前路径祖父目录".center(100, "-"))
# print(os.path.abspath("../.."))  # /Users/linghuchong/Downloads
# print(os.path.abspath("../../.."))  # /Users/linghuchong


# todo 判断是否存在
# print("判断是否绝对路径(不验证正确性)".center(100, "-"))
# # print(os.path.isabs("/Users/linghuchong/Downloads/51/Python/project/PO/"))
#
# print("判断路径或文件是否存在".center(100, "-"))
# print(os.path.exists("/Users/linghuchong/Downloads/51/Python/project/PO/"))  # True
# print(os.path.exists("/Users/linghuchong/Downloads/51/Python/project/PO/os1.py"))  # # True
#
# print("判断目录是否存在".center(100, "-"))
# print(os.path.isdir("/Users/linghuchong/Downloads/51/Python/project/PO/"))  # True   //绝对路径
# print(os.path.isdir("./data"))  # True   //相对路径

print("判断文件是否存在".center(100, "-"))
print(os.path.isfile("/Users/linghuchong/Downloads/51/Python/project/PO/FilePO.py"))  # True   //绝对路径
print(os.path.isfile("./data/1.jpg"))  # True    //相对路径
# # 文件是否存在
# print(os.access("./data/1.jpg", os.F_OK))
# # 文件是否可读
# print(os.access("./data/1.jpg", os.R_OK))
# # 文件是否可以写入
# print(os.access("./data/1.jpg", os.W_OK))
# # 文件是否可以执行
# print(os.access("./data/1.jpg", os.X_OK))



# todo 创建/删除/重命名
# print("新建目录(如果已存在则忽略)".center(100, "-"))
# os.mkdir("/Users/linghuchong/Downloads/51/Python/project/PO/SQL3")

# print("新建多级目录(如果已存在则报错)".center(100, "-"))
# os.makedirs("/Users/linghuchong/Downloads/51/Python/project/PO/SQL1/1/2/3/4")

# print("删除空目录".center(100, "-"))
# os.rmdir("/Users/linghuchong/Downloads/51/Python/project/PO/SQL3")

# print("递归删除所有空目录".center(100, "-"))
# os.removedirs("/Users/linghuchong/Downloads/51/Python/project/PO/SQL2/1/2/3/4")

# print("强制删除目录".center(100, "-"))
# shutil.rmtree(varFolder)

# print("删除文件".center(100, "-"))
# os.remove("/Users/linghuchong/Downloads/51/Python/project/PO/SQL1/1.jpg")

# print("创建空文件(未成功)".center(100, "-"))
# # mode = 0600|stat.S_IRUSR
# # os.mknod("/Users/linghuchong/Downloads/51/Python/project/PO/SQL2/test123.txt", mode)
#
# print("重命名文件或目录".center(100, "-"))
# # os.rename("/Users/linghuchong/Downloads/51/Python/project/socket1.py", "/Users/linghuchong/Downloads/51/Python/project/test12.py")  # 重命名文件
# # os.rename("/Users/linghuchong/Downloads/51/Python/project/PO/SQL1", "/Users/linghuchong/Downloads/51/Python/project/PO/SQL2")  # 重命名目录
#
# print("修改文件权限和时间戳".center(100, "-"))
# # os.chmod(file)

# print("分割文件名和扩展名(不校验正确性)".center(100, "-"))
# print(os.path.splitext("/Users/linghuchong/Downloads/51/Python/project/getYesterday.py"))  # ('/Users/linghuchong/Downloads/51/Python/project/test2', '.py')
# print(os.path.splitext("/Users/linghuchong/Downloads/51/Pyth2on/proj2ect/t.est2.py"))  # ('/Users/linghuchong/Downloads/51/Python/project/test2', '.py')
#
# print("分割路径和文件名(不校验正确性)".center(100, "-"))
# print(os.path.split("/Users/linghuchong/Downloads/51/Python/proj2ect/getYesterday.py"))  # ('/Users/linghuchong/Downloads/51/Python/project', 'getYesterday.py')




# todo 4,获取目录与文件

# print("获取所有子目录名、文件及隐藏文件".center(100, "-"))
# print(os.listdir("/Users/linghuchong/Downloads/51/Python/project/SQL"))  # ['my.cnf', '.DS_Store', 'test', 'employee_connection.txt', 'employee_address.txt', 'text.txt', 'employee.txt', 'docker_mysql.sql']

# print("获取当前目录下所有文件/获取带路径目录下所有文件".center(100, "-"))
# print(glob.glob("*.*"))  # ['PyInstaller-3.5.tar.gz', 'mysqlclient-1.4.4-cp38-cp38-win_amd64.whl', '插件清单.txt', ] //所有文件
# print(glob.glob("*.xlsx"))  # ['插件清单.txt', 'requirements.txt', 'Python+Selenium使用Page Object实现页面自动化测试.txt', '1安装与配置.txt']  //所有txt文件
# print(glob.glob("/Users/linghuchong/*.*"))  # ['/Users/linghuchong/Thumbs.db', '/Users/linghuchong/jmeter.log', '/Users/linghuchong/chcRule.sh', '/Users/linghuchong/ImageMagick-7.0.10-10', '/Users/linghuchong/fineagent.jar']


# print("遍历目录及子目录下文件".center(100, "-"))
# # s_path是路径，l_folder是目录，l_file是文件
# 当 topdown=True（默认值），先遍历根目录，再遍历子目录
# for s_path, l_folder, l_file in os.walk("/Users/linghuchong/Downloads/51/Python/project/SQL"):
#     print(s_path, l_folder, l_file)
# /Users/linghuchong/Downloads/51/Python/project/SQL ['test'] ['my.cnf', '.DS_Store', 'employee_connection.txt', 'employee_address.txt', 'text.txt', 'employee.txt', 'docker_mysql.sql']
# /Users/linghuchong/Downloads/51/Python/project/SQL/test [] ['hello.txt']
# 当 topdown=False，先遍历子目录
# for s_path, l_folder, l_file in os.walk("/Users/linghuchong/Downloads/51/Python/project/SQL", topdown=False):
#     print(s_path, l_folder, l_file)
# /Users/linghuchong/Downloads/51/Python/project/SQL/test [] ['hello.txt']
# /Users/linghuchong/Downloads/51/Python/project/SQL ['test'] ['my.cnf', '.DS_Store', 'employee_connection.txt', 'employee_address.txt', 'text.txt', 'employee.txt', 'docker_mysql.sql']


# print("连接目录与文件名(不验证正确性)".center(100, "-"))
# print(os.path.join(os.getcwd(), "ddd"))  # /Users/linghuchong/Downloads/51/Python/ddd
# print(os.path.join(os.getcwd(), "ddd", "eee", 'fff'))  # /Users/linghuchong/Downloads/51/Python/ddd/eee/fff
# print(os.path.join(os.getcwd(), "/ddd"))  # /ddd
# print(os.path.join(os.getcwd(), "\ddd"))  # /Users/linghuchong/Downloads/51/Python/\ddd
# print(os.path.join(os.getcwd(), "\ddd", "eee"))  # /Users/linghuchong/Downloads/51/Python/\ddd/eee
# print(os.path.join(os.getcwd(), "\ddd", "/eee"))  # /eee

# print("获取文件名".center(100, "-"))
# print(os.path.basename("/Users/linghuchong/Downloads/51/Python/project/getYesterday.py"))  # getYesterday.py
#
# print("获取文件类型".center(100, "-"))
# print(mimetypes.guess_type('/Users/linghuchong/jmeter.log'))  # ('text/plain', None)
# print(mimetypes.guess_type('/Users/linghuchong/chcRule.sh'))  # ('application/x-sh', None)
# print(mimetypes.guess_type('/Users/linghuchong/fineagent.jar'))  # ('application/java-archive', None)
#
# print("获取文件大小".center(100, "-"))
# print(os.path.getsize("/Users/linghuchong/Downloads/51/Python/project/socket1.py"))  # 19964
#
# print("获取文件属性".center(100, "-"))
# print(os.stat("/Users/linghuchong/Downloads/51/Python/project/getYesterday.py")) # os.stat_result(st_mode=33188, st_ino=8624741169, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=5097, st_atime=1709374037, st_mtime=1669197988, st_ctime=1669197988)

# print("获取文件最后修改日期和时间".center(100, "-"))
# # 将修改时间转换为日期格式
# from datetime import datetime
# dateTime = datetime.fromtimestamp(os.path.getmtime('/Users/linghuchong/Downloads/51/Python/project/PO/data/1.jpg' ))
# print(dateTime)  # 2024-12-19 12:29:17.617578




# todo 系统级
# os.system()  # 运行shell命令
# os.exit()  # 终止当前进程

# print("获取系统平台".center(100, "-"))
# print(os.name)  # posix  // mac或linux返回 posix， windows返回 nt
#
# print("获取环境变量".center(100, "-"))
# # print(os.environ.keys()) # KeysView(environ({'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\ZY\\AppData\\Roaming', 'CLASSPATH': '.;C:\\Program Files\\JAVA\\jdk1.8.0_211/lib/dt.jar;C:\\Program Files\\JAVA\\jdk1.8.0_211/lib/tools.jar;', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'DESKTOP-EOCO1V0', 'COMSPEC': 'C:\\Windows\\system32\\cmd.exe', 'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 'FPS_BROWSER_APP_PROFILE_STRING': 'Internet Explorer', 'FPS_BROWSER_USER_PROFILE_STRING': 'Default', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\ZY', 'JAVA_HOME': 'C:\\Program Files\\JAVA\\jdk1.8.0_211', 'JMETER_HOME': 'C:\\apache-jmeter-5.1.1', 'LOCALAPPDATA': 'C:\\Users\\ZY\\AppData\\Local', 'LOGONSERVER': '\\\\DESKTOP-EOCO1V0', 'MYSQL_HOME': 'c:\\mysql-8.0.18-winx64', 'NUMBER_OF_PROCESSORS': '4', 'ONEDRIVE': 'C:\\Users\\ZY\\OneDrive', 'OS': 'Windows_NT', 'PATH': 'C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Windows\\System32\\OpenSSH\\;C:\\Program Files (x86)\\NVIDIA Corporation\\PhysX\\Common;C:\\Program Files\\NVIDIA Corporation\\NVIDIA NvDLISR;C:\\Program Files\\Git\\cmd;C:\\Program Files (x86)\\Windows Kits\\8.1\\Windows Performance Toolkit\\;C:\\Python38\\Scripts\\;C:\\Python38\\;C:\\Users\\ZY\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\ZY\\AppData\\Local\\Programs\\Fiddler;C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\bin;;d:\\myLNK;C:\\mysql-8.0.18-winx64\\bin;', 'PATHEXT': '.exe;.doc;.txt;.xlsx;.lnk;.url;.bat;', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 158 Stepping 9, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': '9e09', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PSMODULEPATH': 'C:\\Program Files\\WindowsPowerShell\\Modules;C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\Modules', 'PUBLIC': 'C:\\Users\\Public', 'PYCHARM': 'C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\bin;', 'PYCHARM_HOSTED': '1', 'PYCHARM_MATPLOTLIB_PORT': '53639', 'PYTHONIOENCODING': 'UTF-8', 'PYTHONPATH': 'D:\\51\\python\\project;C:\\Program Files\\JetBrains\\PyCharm 2018.3.5\\helpers\\pycharm_matplotlib_backend', 'PYTHONUNBUFFERED': '1', 'SESSIONNAME': 'Console', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\Windows', 'TEMP': 'C:\\Users\\ZY\\AppData\\Local\\Temp', 'TESSDATA_PREFIX': 'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata', 'TMP': 'C:\\Users\\ZY\\AppData\\Local\\Temp', 'USERDOMAIN': 'DESKTOP-EOCO1V0', 'USERDOMAIN_ROAMINGPROFILE': 'DESKTOP-EOCO1V0', 'USERNAME': 'ZY', 'USERPROFILE': 'C:\\Users\\ZY', 'VS140COMNTOOLS': 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\Common7\\Tools\\', 'WINDIR': 'C:\\Windows'}))
# for win
# print(os.environ['HOMEPATH'])  # \Users\ZY   //当前用户主目录。
# print(os.environ['TEMP'])  # C:\Users\ZY\AppData\Local\Temp   //# 临时目录路径。
# print(os.environ['PATHEXT'])  # .exe;.doc;.txt;.xlsx;.lnk;.url;.bat;   //# 可执行文件。
# print(os.environ['SYSTEMROOT'])  # C:\Windows  //# 系统主目录。
# print(os.environ['LOGONSERVER'])  # \\DESKTOP-EOCO1V0  /# 机器名。
# print(os.getenv("JAVA_HOME"))  # C:\Program Files\JAVA\jdk1.8.0_211
# for mac
# print(os.getenv("JAVA_HOME"))  # /Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home

# print("添加路径到系统环境变量".center(100, "-"))
# # sys.path.append("D:\\51\\python\\project\\PO")
# # print(sys.path)
# #
# #
# print("根据环境变量的值替换path".center(100, "-"))
# # # 1.3 os.path.expandvars(path)，根据环境变量的值替换path中包含的”$name”和”${name}”
# # os.environ['testPATH'] = 'D:/thunder'
# # path = '$testPATH/train/13.png'
# # print(os.path.expandvars(path))  # D:/thunder/train/13.png
#
#




