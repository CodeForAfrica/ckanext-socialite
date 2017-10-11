import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class LinkedInTestCase(unittest.TestCase):
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
		button_link = driver.find_element_by_xpath(u'//a[@id="linkedin-btn"]')
		assert button_link

	def testPopUpWindow(self):
		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		main_window_title = driver.title
		main_window_handle = driver.window_handles[0]
		driver.find_element_by_id('linkedin-btn').click()
		signin_window_handle = driver.window_handles[1]
		driver.switch_to.window(signin_window_handle)
		try:
			WebDriverWait(driver, 10).until(EC.title_contains("Authorize | LinkedIn"))
			signin_window_title = driver.title
			self.assertNotEqual(main_window_title,signin_window_title)
		finally:
			driver.quit()

	def testPopUpContent(self):
		driver = self.browser
		driver.implicitly_wait(10)
		driver.get('http://localhost:5000/user/login')
		driver.find_element_by_id('linkedin-btn').click()
		signin_window_handle = driver.window_handles[1]
		driver.switch_to.window(signin_window_handle)

		note_wrapper = driver.find_element_by_class_name('note')
		note_wrapper_text = note_wrapper.text
		expected_note_text = 'ckanext-socialite would like to access some of your LinkedIn info:'
		self.assertEqual(note_wrapper_text,expected_note_text)

	def testSuccessfulLogin(self):
		driver = self.browser
		driver.implicitly_wait(50)
		driver.get('http://localhost:5000/user/login')

		driver.find_element_by_id('linkedin-btn').click()
		main_window_handle = driver.window_handles[0]
		signin_window_handle = driver.window_handles[1]
		driver.switch_to.window(signin_window_handle)
		submit_button = driver.find_element_by_class_name('allow.btn-primary')
		email_input = driver.find_element_by_id('session_key-oauthAuthorizeForm').send_keys('buzzdhani@hotmail.com')
		password_input = driver.find_element_by_id('session_password-oauthAuthorizeForm').send_keys('ckanext-socialite')
		submit_button.submit()
		driver.switch_to.window(main_window_handle)
		try:
			WebDriverWait(driver, 20).until(EC.title_contains("Datasets - CKAN"))
			self.assertEqual(driver.title, 'Datasets - CKAN')
		finally:
			driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)

