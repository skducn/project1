"""
@Version: 1.0
@Project: BeautyReport
@Author: Raymond
@Data: 2017/11/15 下午5:28
@File: __init__.py.py
@License: MIT
"""

import os
import sys
from io import StringIO as StringIO
import time
import json
import unittest
import platform
import base64
from distutils.sysconfig import get_python_lib
import traceback
from functools import wraps

import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
private_key = RSA.import_key(open("private_key.pem", "rb").read())
cipher = PKCS1_OAEP.new(private_key)
encrypted_data = open("encrypted_data.bin", "rb").read()
data = cipher.decrypt(encrypted_data)
projectName = data.decode("utf-8", 'strict')  # 将 bytes转换成字符串

__all__ = ['BeautifulReport']

HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}">
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    
    def __init__(self, fp):
        self.fp = fp
    
    def write(self, s):
        self.fp.write(s)
    
    def writelines(self, lines):
        self.fp.writelines(lines)
    
    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

SYSSTR = platform.system()
SITE_PAKAGE_PATH = get_python_lib()

FIELDS = {
    "testPass": 0,
    "testResult": [
    ],
    "iDoc": "",
    "iEnv": "",
    "iDatabase": "",
    "test": "",
    "testAll": 0,
    "testFail": 0,
    "beginTime": "",
    "totalTime": "",
    "testSkip": 0
}


class PATH:
    """ all file PATH meta """
    # config_tmp_path = SITE_PAKAGE_PATH + '/BeautifulReport/template/template'
    config_tmp_path = os.getcwd() + "/template"
    # print(config_tmp_path)

class MakeResultJson:
    """ make html table tags """
    
    def __init__(self, datas: tuple):
        """
        init self object
        :param datas: 拿到所有返回数据结构
        """
        self.datas = datas
        self.result_schema = {}
    
    def __setitem__(self, key, value):
        """
        
        :param key: self[key]
        :param value: value
        :return:
        """
        self[key] = value
    
    def __repr__(self) -> str:
        """
            返回对象的html结构体
        :rtype: dict
        :return: self的repr对象, 返回一个构造完成的tr表单
        """
        keys = (
            'excelNo',
            'className',
            'testType',
            'testSort',
            'testWay',
            'description',
            'testDate',
            'spendTime',
            'status',
            'log',
        )
        # keys = (
        #     'className',
        #     'methodName',
        #     'description',
        #     'spendTime',
        #     'status',
        #     'log',
        # )
        # print(self.datas)
        for key, data in zip(keys, self.datas):
            self.result_schema.setdefault(key, data)
        # print(self.result_schema)
        return json.dumps(self.result_schema)


class ReportTestResult(unittest.TestResult):
    """ override"""
    
    def __init__(self, suite, stream=sys.stdout):
        """ pass """

        super(ReportTestResult, self).__init__()
        self.begin_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.start_time = 0
        self.stream = stream
        self.end_time = 0
        self.failure_count = 0
        self.error_count = 0
        self.success_count = 0
        self.skipped = 0
        self.verbosity = 1
        self.success_case_info = []
        self.skipped_case_info = []
        self.failures_case_info = []
        self.errors_case_info = []
        self.all_case_counter = 0
        self.suite = suite
        self.status = ''
        self.result_list = []
        self.case_log = ''
        self.default_report_name = '自动化测试报告'
        self.FIELDS = None
        self.sys_stdout = None
        self.sys_stderr = None
        self.outputBuffer = None
    
    @property
    def success_counter(self) -> int:
        """ set success counter """
        return self.success_count
    
    @success_counter.setter
    def success_counter(self, value) -> None:
        """
            success_counter函数的setter方法, 用于改变成功的case数量
        :param value: 当前传递进来的成功次数的int数值
        :return:
        """
        self.success_count = value
    
    def startTest(self, test) -> None:
        """
            当测试用例测试即将运行时调用
        :return:
        """
        unittest.TestResult.startTest(self, test)
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.sys_stdout = sys.stdout
        self.sys_stdout = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector
        self.start_time = time.time()
    
    def stopTest(self, test) -> None:
        """
            当测试用力执行完成后进行调用
        :return:
        """
        self.end_time = '{0:.2} 秒'.format((time.time() - self.start_time))
        # print(test.__dict__)
        # print(test.__dict__['_testMethodDoc'].split("caseQty=")[1].split("]")[0])
        self.caseQty = test.__dict__['_testMethodDoc'].split("caseQty=")[1].split("]")[0]

        self.result_list.append(self.get_all_result_info_tuple(test))
        # print(self.result_list)
        self.complete_output()
    
    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.sys_stdout:
            sys.stdout = self.sys_stdout
            sys.stderr = self.sys_stdout
            self.sys_stdout = None
            self.sys_stdout = None
        return self.outputBuffer.getvalue()
    
    def stopTestRun(self, title=None) -> dict:
        """
            所有测试执行完成后, 执行该方法
        :param title:
        :return:
        """

        for item in self.result_list:
            item = json.loads(str(MakeResultJson(item)))
            FIELDS.get('testResult').append(item)
        FIELDS['projectName'] = projectName
        FIELDS['iDoc'] = title if title else self.default_report_name
        FIELDS['iEnv'] = localReadConfig.get_env("switchenv")
        if localReadConfig.get_env("switchenv") == "test":
            FIELDS['iDatabase'] = localReadConfig.get_test("db_database")
        elif localReadConfig.get_env("switchenv") == "dev":
            FIELDS['iDatabase'] = localReadConfig.get_dev("db_database")
        FIELDS['testAll'] = self.caseQty
        # FIELDS['testAll'] = len(self.result_list)
        FIELDS['testPass'] = self.success_counter
        FIELDS['testFail'] = self.failure_count
        # FIELDS['testSkip'] = self.skipped
        FIELDS['testSkip'] = int(self.caseQty) - int(self.success_counter) - int(self.failure_count)
        FIELDS['beginTime'] = self.begin_time
        end_time = int(time.time())
        start_time = int(time.mktime(time.strptime(self.begin_time, '%Y-%m-%d %H:%M:%S')))
        FIELDS['totalTime'] = str(end_time - start_time) + '秒'
        FIELDS['testError'] = self.error_count
        self.FIELDS = FIELDS
        # print(FIELDS)
        return FIELDS
    
    def get_all_result_info_tuple(self, test) -> tuple:
        """
            接受test 相关信息, 并拼接成一个完成的tuple结构返回
        :param test:
        :return:
        """
        return tuple([*self.get_testcase_property(test), self.end_time, self.status, self.case_log])
    
    @staticmethod
    def error_or_failure_text(err) -> str:
        """
            获取sys.exc_info()的参数并返回字符串类型的数据, 去掉t6 error
        :param err:
        :return:
        """
        return traceback.format_exception(*err)
    
    def addSuccess(self, test) -> None:
        """
            pass
        :param test:
        :return:
        """
        logs = []
        output = self.complete_output()
        logs.append(output)
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')
        self.success_counter += 1
        self.status = '成功'
        self.case_log = output.split('\n')
        self._mirrorOutput = True  # print(class_name, method_name, method_doc)
    
    def addError(self, test, err):
        """
            add Some Error Result and infos
        :param test:
        :param err:
        :return:
        """
        logs = []
        output = self.complete_output()
        logs.append(output)
        logs.extend(self.error_or_failure_text(err))
        self.failure_count += 1
        self.add_test_type('失败', logs)
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')
        
        self._mirrorOutput = True
    
    def addFailure(self, test, err):
        """
            add Some Failures Result and infos
        :param test:
        :param err:
        :return:
        """
        logs = []
        output = self.complete_output()
        logs.append(output)
        logs.extend(self.error_or_failure_text(err))
        self.failure_count += 1
        self.add_test_type('失败', logs)
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')
        
        self._mirrorOutput = True
    
    def addSkip(self, test, reason) -> None:
        """
            获取全部的跳过的case信息
        :param test:
        :param reason:
        :return: None
        """
        logs = [reason]
        self.complete_output()
        self.skipped += 1
        self.add_test_type('跳过', logs)
        
        if self.verbosity > 1:
            sys.stderr.write('S  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('S')
        self._mirrorOutput = True
    
    def add_test_type(self, status: str, case_log: list) -> None:
        """
            abstruct add test type and return tuple
        :param status:
        :param case_log:
        :return:
        """
        self.status = status
        self.case_log = case_log
    
    @staticmethod
    def get_testcase_property(test) -> tuple:
        """
            接受一个test, 并返回一个test的class_name, method_name, method_doc属性
        :param test:
        :return: (class_name, method_name, method_doc) -> tuple
        """
        # class_name = test.__class__.__qualname__
        # print(test.__dict__)
        # method_name = test.__dict__['_testMethodName']
        # method_doc = test.__dict__['_testMethodDoc']
        # print(class_name)
        # print(method_name)
        # print(method_doc)
        # method_doc = test.__dict__['_testMethodDoc'].split("iName=")[1].split(",")[0]
        # print(test.__dict__)
        excelNo = test.__dict__['_testMethodDoc'].split("excelNo=")[1].split(",")[0]
        class_name = test.__dict__['_testMethodDoc'].split("tester='")[1].split("'")[0]
        testType = test.__dict__['_testMethodDoc'].split("iType='")[1].split("'")[0]
        testSort = test.__dict__['_testMethodDoc'].split("iSort='")[1].split("'")[0]
        testWay = test.__dict__['_testMethodDoc'].split("iMethod='")[1].split("'")[0]
        testCaseName = test.__dict__['_testMethodDoc'].split("iName='")[1].split("'")[0]
        testDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        # print(excelNo, class_name, testType, testSort, testCaseName, testDate)
        # return class_name, method_name, method_doc
        return excelNo, class_name, testType, testSort, testWay, testCaseName, testDate


class BeautifulReport(ReportTestResult, PATH):
    img_path = 'img/' if platform.system() != 'Windows' else 'img\\'
    
    def __init__(self, suites):
        super(BeautifulReport, self).__init__(suites)
        self.suites = suites
        self.log_path = None
        self.title = '自动化测试报告'
        self.filename = 'report.html'

    def report(self, description, filename: str = None, log_path='.'):
        """
            生成测试报告,并放在当前运行路径下
        :param log_path: 生成report的文件存储路径
        :param filename: 生成文件的filename
        :param description: 生成文件的注释
        :return:
        """
        if filename:
            self.filename = filename if filename.endswith('.html') else filename + '.html'
        
        if description:
            self.title = description

        self.log_path = os.path.abspath(log_path)
        self.suites.run(result=self)
        self.stopTestRun(self.title)
        self.output_report()
        # text = '\n执行完毕, 可前往{}查询测试报告'.format(self.log_path)
        # print('\nDone')
    
    def output_report(self):
        """
            生成测试报告到指定路径下
        :return:
        """
        template_path = self.config_tmp_path
        override_path = os.path.abspath(self.log_path) if \
            os.path.abspath(self.log_path).endswith('/') else \
            os.path.abspath(self.log_path) + '/'
        
        with open(template_path, 'rb') as file:
            body = file.readlines()
        with open(override_path + self.filename, 'wb') as write_file:
            for item in body:
                if item.strip().startswith(b'var resultData'):
                    head = '    var resultData = '
                    item = item.decode().split(head)
                    item[1] = head + json.dumps(self.FIELDS, ensure_ascii=False, indent=4)
                    item = ''.join(item).encode()
                    item = bytes(item) + b';\n'
                write_file.write(item)
    
    @staticmethod
    def img2base(img_path: str, file_name: str) -> str:
        """
            接受传递进函数的filename 并找到文件转换为base64格式
        :param img_path: 通过文件名及默认路径找到的img绝对路径
        :param file_name: 用户在装饰器中传递进来的问价匿名
        :return:
        """
        pattern = '/' if platform != 'Windows' else '\\'

        with open(img_path + pattern + file_name, 'rb') as file:
            data = file.read()
        return base64.b64encode(data).decode()

    def add_test_img(*pargs):
        """
            接受若干个图片元素, 并展示在测试报告中
        :param pargs:
        :return:
        """

        def _wrap(func):
            @wraps(func)
            def __wrap(*args, **kwargs):
                img_path = os.path.abspath('{}'.format(BeautifulReport.img_path))
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    if 'save_img' in dir(args[0]):
                        save_img = getattr(args[0], 'save_img')
                        save_img(func.__name__)
                        data = BeautifulReport.img2base(img_path, pargs[0] + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    sys.exit(0)
                print('<br></br>')

                if len(pargs) > 1:
                    for parg in pargs:
                        print(parg + ':')
                        data = BeautifulReport.img2base(img_path, parg + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    return result
                if not os.path.exists(img_path + pargs[0] + '.png'):
                    return result
                data = BeautifulReport.img2base(img_path, pargs[0] + '.png')
                print(HTML_IMG_TEMPLATE.format(data, data))
                return result
            return __wrap
        return _wrap
