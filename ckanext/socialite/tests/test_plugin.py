"""Tests for plugin.py."""
import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class AuthTests(unittest.TestCase):
    """This class describes the tests for the Authentication."""

    def setUp(self):
        """This prepares the test environment.
        """
        self.driver = webdriver.Chrome("/usr/local/lib/ckan/default/bin/chromedriver")
        self.driver.get("localhost:5000/user/login")
        self.driver.implicitly_wait(10)
        self.username_input = os.getenv("test_username")
        self.password_input = os.getenv("test_password")

    def tearDown(self):
        """This destroys the test environment."""
        self.driver.quit()

    def test_githubauth(self):
        """This function tests if the Authentication Process works correctly with the Project.
        """
        ckan_window = self.driver.window_handles[0]
        github_signin = self.driver.find_element_by_id("github-button")
        github_signin.click()
        auth_window = self.driver.window_handles[1]
        self.driver.switch_to_window(auth_window)
        username = self.driver.find_element_by_xpath('//*[@id="login_field"]')
        username.send_keys(self.username_input)
        password_field = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_field.send_keys(self.password_input)
        password_field.send_keys(u'\ue007')
        self.driver.implicitly_wait(10 * 1000)
        auth_button = self.driver.find_element_by_xpath('//*[@id="js-oauth-authorize-btn"]')
        if auth_button is not None:
            auth_button.send_keys(u'\ue007')
        else:
            pass
        self.driver.switch_to_window(ckan_window)
        self.driver.implicitly_wait(10 * 1000)
        time.sleep(10)
        url_now = self.driver.current_url
        print(url_now)
        self.assertEqual('http://localhost:5000/dataset', url_now)
