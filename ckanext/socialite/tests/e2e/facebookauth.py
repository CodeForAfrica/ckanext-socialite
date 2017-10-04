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

	def testPageTitle(self):
		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		assert 'Login - CKAN' in driver.title

	def testButtonRender(self):
		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		frame = driver.find_element_by_xpath(u'//iframe[@title = "fb:login_button Facebook Social Plugin"]')	
		try: 
			WebDriverWait(driver, 300).until(EC.frame_to_be_available_and_switch_to_it(frame))
			wait = WebDriverWait(driver, 10)
			element = wait.until(element_has_css_class((By.ID, 'u_0_1'), "_xvm _29o8"))
			self.assertIn('Continue with Facebook', element.text)
		finally:
			driver.quit()

	def testPopUpContent(self):
		driver = self.browser
		driver.implicitly_wait(10)
		driver.get('http://localhost:5000/user/login')
		frame = driver.find_element_by_xpath(u'//iframe[@title = "fb:login_button Facebook Social Plugin"]')
		try:
			WebDriverWait(driver, 300).until(EC.frame_to_be_available_and_switch_to_it(frame))
			element = WebDriverWait(driver, 10).until(element_has_css_class((By.ID, 'u_0_1'), "_xvm _29o8"))
			element.click()
			signin_window_handle = driver.window_handles[1]
			driver.switch_to.window(signin_window_handle)
			content_wrapper = driver.find_element_by_id('content')
			content_wrapper_text = content_wrapper.text
			expected_content_text = 'Log in to use your Facebook account with Ckanext-socialite.'
			self.assertIn(expected_content_text,content_wrapper_text)
		finally:
			driver.quit()

	def testSuccessfulLogin(self):
		driver = self.browser
		driver.implicitly_wait(50)
		driver.get('http://localhost:5000/user/login')
		frame = driver.find_element_by_xpath(u'//iframe[@title = "fb:login_button Facebook Social Plugin"]')
		try:
			WebDriverWait(driver, 300).until(EC.frame_to_be_available_and_switch_to_it(frame))
			element = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.ID, 'u_0_1')))
			element.click()
			WebDriverWait(driver, 100)
			driver.switch_to.default_content()
			main_window_handle = driver.window_handles[0]
			signin_window_handle = driver.window_handles[1]
			driver.switch_to.window(signin_window_handle)
			email_input = driver.find_element_by_id('email').send_keys('buzzdhani@hotmail.com')
			password_input = driver.find_element_by_id('pass').send_keys('ckanext&socialite')
			submit_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.NAME, 'login')))
			submit_button.submit()
			driver.switch_to.window(main_window_handle)
			WebDriverWait(driver, 20).until(EC.title_contains("Datasets - CKAN"))
			self.assertIn(driver.title, 'Datasets - CKAN')
		finally:
			driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)

