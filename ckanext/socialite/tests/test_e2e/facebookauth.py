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
		driver.get('http://localhost:5000/user/login')
		button_link = driver.find_element_by_xpath(u'//a[@id="linkedin-btn"]')
		assert button_link

	def testPopUpContent(self):
		driver = self.browser
		driver.implicitly_wait(10)
		driver.get('http://localhost:5000/user/login')
		main_window_handle = driver.window_handles[0]
		driver.find_element_by_id('facebook-btn').click()
		signin_window_handle = driver.window_handles[1]
		driver.switch_to.window(signin_window_handle)
		
		content_wrapper = driver.find_element_by_id('content')
		content_wrapper_text = content_wrapper.text
		expected_content_text = 'Log in to use your Facebook account with Ckanext-socialite.'
		self.assertIn(expected_content_text,content_wrapper_text)
		

	def testSuccessfulLogin(self):
		driver = self.browser
		driver.implicitly_wait(50)
		driver.get('http://localhost:5000/user/login')
		button_link = driver.find_element_by_xpath(u'//a[@id="facebook-btn"]')
		try:
			button_link.click()
			main_window_handle = driver.window_handles[0]
			signin_window_handle = driver.window_handles[1]
			driver.switch_to.window(signin_window_handle)
			email_input = driver.find_element_by_id('email').send_keys('d.abelega@cannonprojects.com')
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

