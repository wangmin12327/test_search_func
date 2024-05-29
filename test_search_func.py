import logging
import time
import webbrowser

import allure
import pytest
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from log.log_utils import logger

"""
-------------------------------------------------------------
tittle: 测试人搜索功能

优先级：

前置条件： 打开浏览器

测试步骤；
        1、进入测试人论坛搜索页面,截图
        2、输入搜索关键词；
        3、点击搜索按钮；
预期结果：
        1、搜索成功；
        2、搜索结果列表包含关键字；
--------------------------------------------------------------

作者：wang-min
创建时间：2024.05.13
"""


class TestCeShiRen:
    def get_screen_shot(self):
        """
        获取截图
        1、定义时间戳
        2、提前创建截图存放路径image_path
        3、通过save_screenshot函数生成截图,并将截图存放到image_path路径
        4、将生成好的截图通过allure.attach.file方式附在allure测试报告中
        :return:
        """
        # 时间戳需要转为整型输出
        self.time_tamp = int(time.time())
        self.image_path = f"./images/image_{self.time_tamp}.png"
        self.driver.save_screenshot(self.image_path)
        allure.attach.file(self.image_path, name="picture", attachment_type=allure.attachment_type.PNG)

    def get_page_source(self):
        """
        获取网页html源码，帮助调试
        1、获取目标网页的链接地址
        2、打开本地文件，将目标网页html源码写入到本地文件
        :return:
        """
        self.driver.get("https://ceshiren.com/")
        with open("page_source/page_source.html", "w", encoding="utf8") as f:
            f.write(self.driver.page_source)

    def setup_class(self):
        """
        前置条件： 打开浏览器
        """
        # 打开浏览器
        self.driver = webdriver.Chrome()

        # 设置3秒隐式等待
        self.driver.implicitly_wait(3)

    def teardown_class(self):
        """
        后置条件： 销毁chromedriver进程, 并关闭浏览器
        :return:
        """
        self.driver.quit()

    # 参数化搜索关键字
    @pytest.mark.parametrize("send_keys", ["Selenium", "Appium", "面试"])
    def test_search(self, send_keys):
        """
        1、打开测试人论坛，截图；
        2、跳转到高级搜索页面，添加显式等待判断页面跳转成功并截图；
        3、搜索输入框输入搜索关键字，截图；
        4、打印当前结果页面的pagesource并截图；
        5、断言：第一个标题是否包含关键字

        :return: 预期结果/实际结果
        """
        # 打开测试人论坛，截图
        self.driver.get("https://ceshiren.com/")
        self.get_screen_shot()

        # 1、跳转到高级搜索页面，添加显式等待判断页面跳转成功并截图
        # 首先，点击搜索按钮
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//*[@id='search-button']").click()

        # 然后，点击"打开高级搜索"按钮,跳转到高级搜索页面
        # 添加显式等待判断页面跳转成功
        ele = WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//*[@title='打开高级搜索']")))
        # self.driver.find_element(By.XPATH, "//*[@title='打开高级搜索']").click()
        ele.click()
        # 截图
        self.get_screen_shot()

        # 2、搜索输入框输入搜索关键字，截图
        # 考虑特殊场景的验证: 输入内容过长,特殊字符,其他
        if len(send_keys) > 8:
            logger.debug("搜索框输入的字符长度过长！")
        elif type(send_keys) == "[]":
            logger.debug("搜索框输入的字符类型不合法！")
        else:
            time.sleep(3)
            self.driver.find_element(By.CSS_SELECTOR, "[placeholder = '搜索']").send_keys(send_keys)
        self.get_screen_shot()

        # 3、打印当前结果页面的pagesource并截图。
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, ".search-cta").click()
        self.get_screen_shot()
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder = '搜索']").clear()

        # 4、打印搜索结果的第一个标题
        # 获取包含搜索关键字列表中的第一个搜索结果，web_element对象，定位到该元素对象
        ele1 = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".topic "
                                                                                ".topic-title>.ember-view")))
        print(ele1)
        # 截图
        self.get_screen_shot()

        # 5、断言：第一个标题是否包含关键字
        # 获取元素对象的文本信息(text), 进行断言, 判断关键字是否在获取的实际结果文本之中
        assert send_keys.lower() in ele1.text
        logger.info(f"关键字{send_keys}在搜索结果列表的第一个搜索结果{ele1}中")
        self.get_page_source()
