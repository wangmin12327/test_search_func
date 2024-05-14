import time
import webbrowser

import pytest
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
-------------------------------------------------------------
tittle: 测试人搜索功能

优先级：

前置条件： 进入测试人论坛搜索页面

测试步骤；
        1、输入搜索关键词；
        2、点击搜索按钮；
预期结果：
        1、搜索成功；
        2、搜索结果列表包含关键字；
--------------------------------------------------------------

作者：wang-min
创建时间：2024.05.13
"""


class TestCeShiRen:

    def setup_class(self):
        """
        前置条件： 打开浏览器，进入测试人论坛搜索页面
        """
        # 打开浏览器
        self.driver = webdriver.Chrome()

        # 设置3秒隐式等待
        self.driver.implicitly_wait(3)

        # 打开被测地址
        self.driver.get("https://ceshiren.com/search?expanded=true")

    @pytest.mark.parametrize("send_keys", ["Selenium", "Appium", "面试"])
    def test_search(self, send_keys):
        """
        1、输入搜索关键词；
        2、点击搜索按钮；
        :return: 预期结果/实际结果
        """

        # 定位到搜索输入框，并输入搜索内容
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder = '搜索']").send_keys(send_keys)

        # 定位到搜索按钮，并点击
        self.driver.find_element(By.CSS_SELECTOR, ".search-cta").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder = '搜索']").clear()

        # 获取包含搜索关键字列表中的第一个搜索结果，web_element对象，定位到该元素对象
        web_element = self.driver.find_element(By.CSS_SELECTOR, ".topic-title")
        # 获取元素对象的文本信息(text), 进行断言, 判断appium关键字是否在获取的实际结果文本之中
        assert send_keys.lower() in web_element.text.lower()

        print(web_element.text)

    def teardown_class(self):
        """
        后置条件： 销毁chromedriver进程, 并关闭浏览器
        :return:
        """
        self.driver.quit()
