# pip install playwright pytest-playwright pytest
# playwright install

from playwright.sync_api import Page, expect
import pytest

def test_login_pw(page: Page) -> None:
    page.goto("http://116.62.63.211/shop/user/loginInfo.html")
    page.get_by_role(role="textbox", name="请输入用户名/手机/邮箱").fill("beifan")
    page.get_by_role(role="textbox", name="请输入登录密码").fill("beifan")
    page.get_by_role(role="button", name="登录").click()
    expect(page.locator('//p[@class="prompt-msg"]')).to_contain_text("密码错误")