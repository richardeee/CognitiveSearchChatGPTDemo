from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://tis.mindray.com/#/login")
    page.get_by_role("button", name="中国站点").click()
    time.sleep(1)
    page.get_by_placeholder("someone@example.com").click()
    page.get_by_placeholder("someone@example.com").fill("S100009312")
    page.get_by_placeholder("密码").click()
    page.get_by_placeholder("密码").fill("Lxq6284444")
    page.get_by_role("button", name="登录").click()
    time.sleep(1)
    page.get_by_role("button", name="同意", exact=True).click()
    time.sleep(1)
    page.get_by_placeholder("请选择 产品线").click()
    time.sleep(1)
    page.get_by_text("体外诊断").click()
    time.sleep(1)
    page.get_by_placeholder("请选择 机型大类").click()
    time.sleep(1)
    page.get_by_text("发光仪器").click()
    time.sleep(1)
    page.get_by_text("2022-10-11").click()
    page.locator("form").filter(has_text="产品线: 无匹配数据 体外诊断 加载中 机型大类: 无匹配数据 发光仪器 加载中 机器型号: 无匹配数据 CL-6000i 加载中 工艺代号: 无匹配数据 BM").get_by_role("button", name="查询").click()
    time.sleep(1)
    page.get_by_text("手册文档").click()
    time.sleep(1)
    page.get_by_role("textbox", name="请输入").click()
    page.get_by_role("textbox", name="请输入").fill("磁分离")
    page.locator(".ivu-input-group-append").first.click()
    time.sleep(1)
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
