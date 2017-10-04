import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from custom_wait import element_has_css_class

class FacebookTestCase(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.addCleanup(self.browser.quit)

	# def testPageTitle(self):
	# 	driver = self.browser
	# 	driver.get('http://localhost:5000/user/login')
	# 	assert 'Login - CKAN' in driver.title

	def testButtonRender(self):
		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		frame = driver.find_element_by_xpath(u'//iframe[@title = "fb:login_button Facebook Social Plugin"]')
		WebDriverWait(driver, 300).until(EC.frame_to_be_available_and_switch_to_it(frame))
		wait = WebDriverWait(driver, 10)
		element = wait.until(element_has_css_class((By.ID, 'u_0_1'), "_xvm _29o8"))
		self.assertIn('Continue with Facebook', element.text)

if __name__ == '__main__':
    unittest.main(verbosity=2)

