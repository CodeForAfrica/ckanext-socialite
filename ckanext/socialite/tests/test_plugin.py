"""Tests for plugin.py."""
import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class GoogleAuthTests(unittest.TestCase):
    """This class describes the tests for the Google Authentication"""

    def setUp(self):
        """This prepares the test environment"""
        self.driver = webdriver.Chrome("/usr/local/lib/ckan/default/bin/chromedriver")
        self.driver.get("localhost:5000/user/login")
        self.driver.implicitly_wait(10)
        self.username_input = os.getenv("test_username")
        self.password_input = os.getenv("test_password")

    def tearDown(self):
        """This destroys the test environment"""
        self.driver.quit()

    def test_googleauth(self):
        """This function tests if the GoogleAuth works correctly with
        the Project"""
        ckan_window = self.driver.window_handles[0]
        g_signin = self.driver.find_element_by_id("g-signin-button")
        g_signin.click()
        auth_window = self.driver.window_handles[1]
        self.driver.switch_to_window(auth_window)
        username = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        username.send_keys(self.username_input)
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
        password_field = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password_field.send_keys(self.password_input+"\n")
        self.driver.switch_to_window(ckan_window)
        wait = WebDriverWait(self.driver, 20)
        wait.until(lambda driver: driver.current_url != "http://localhost/user/login")
        url_now = self.driver.current_url
        print(url_now)
        # self.assertEqual(url_now, "http://localhost:5000/dataset")
