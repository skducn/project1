# https://www.bilibili.com/video/BV1bt4y147M4?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372


def setup_module():
    print("准备资源： setup module")

def teardown_module():
    print("资源销毁： teardown module")

def test_case1():
    print("case1")

def test_case2():
    print("case2")

def setup_function():
    print("准备资源： setup function")

def teardown_function():
    print("资源销毁： teardown function")


class TestDemo:

    def setup_class(self):
        print("TestDemo setup class")

    def teardown_class(self):
        print("TestDemo teardown class")

    def setup_method(self):
        print("TestDeom setup")

    def teardown_method(self):
        print("TestDeom teardown")

    def test_demo1(self):
        print("test demo1")

    def test_demo2(self):
        print("test demo2")