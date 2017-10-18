import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TestLinkedInAuth(unittest.TestCase):
	"""This class describes the tests for the LinkedIN Authentication."""
	def setUp(self):
		 """This prepares the test environment.
     """
		self.browser = webdriver.Firefox()
		self.addCleanup(self.browser.quit)

	def testPageTitle(self):
		"""Tests that page title is rendered correctly"""

		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		assert 'Login - CKAN' in driver.title

	def testButtonRender(self):
		"""Tests that login button is rendered correctly"""
		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		button_link = driver.find_element_by_xpath(u'//a[@id="linkedin-btn"]')
		assert button_link

	def testPopUpWindow(self):
		"""Tests that pop up window opens when login button is clicked"""
		driver = self.browser
		driver.get('http://localhost:5000/user/login')
		# Find button and assign window handles
		main_window_title = driver.title
		main_window_handle = driver.window_handles[0]
		driver.find_element_by_id('linkedin-btn').click()
		signin_window_handle = driver.window_handles[1]

		# Switch to popup window and examine popup title
		driver.switch_to.window(signin_window_handle)
		try:
			WebDriverWait(driver, 10).until(EC.title_contains("Authorize | LinkedIn"))
			signin_window_title = driver.title
			self.assertNotEqual(main_window_title,signin_window_title)
		finally:
			driver.quit()

	def testPopUpContent(self):
		"""Tests that pop up window renders correct content"""
		driver = self.browser
		driver.implicitly_wait(10)
		driver.get('http://localhost:5000/user/login')

		# Find button and assign window handles
		driver.find_element_by_id('linkedin-btn').click()
		signin_window_handle = driver.window_handles[1]
		driver.switch_to.window(signin_window_handle)

		# Compare expected popup content with atual popup content
		note_wrapper = driver.find_element_by_class_name('note')
		note_wrapper_text = note_wrapper.text
		expected_note_text = 'ckanext-socialite would like to access some of your LinkedIn info:'
		self.assertEqual(note_wrapper_text,expected_note_text)

	def testSuccessfulLogin(self):
		"""Tests that user is redirected to DataSets page on successful login"""
		driver = self.browser
		driver.implicitly_wait(50)
		driver.get('http://localhost:5000/user/login')

		# Find buttons and assign window handles
		driver.find_element_by_id('linkedin-btn').click()
		main_window_handle = driver.window_handles[0]
		signin_window_handle = driver.window_handles[1]
		driver.switch_to.window(signin_window_handle)
		submit_button = driver.find_element_by_class_name('allow.btn-primary')

		# Input user credentials and submit
		email_input = driver.find_element_by_id('session_key-oauthAuthorizeForm').send_keys('buzzdhani@hotmail.com')
		password_input = driver.find_element_by_id('session_password-oauthAuthorizeForm').send_keys('ckanext-socialite')
		submit_button.submit()

		# Move away from popup window to main window
		driver.switch_to.window(main_window_handle)
		try:
			WebDriverWait(driver, 20).until(EC.title_contains("Datasets - CKAN"))
			self.assertEqual(driver.title, 'Datasets - CKAN')
		finally:
			driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
