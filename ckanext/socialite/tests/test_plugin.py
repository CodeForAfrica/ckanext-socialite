"""Tests for plugin.py."""
import unittest
from ckanext.socialite import plugin
from mock import MagicMock

class SocialitePluginTest(unittest.TestCase):
    def setUp(self):

        self._toolkit = plugin.toolkit
        plugin.toolkit = MagicMock()

    def tearDown(self):
        plugin.toolkit = self._toolkit
        
    def test_update_config(self):
        # Create instance
        self.socialite_instance = plugin.SocialitePlugin()
        # Test
        config = MagicMock()
        self.socialite_instance.update_config(config)
        plugin.toolkit.add_template_directory.assert_called_once_with(config, 'templates')

    def test_login(self):
        params = ([('name', 'Shani Agent'), ('email', 'buzzdhani@hotmail.com'), ('id_token', 'sPDwypON4z')])
        user_account = params[1][1].split('@')[0]

        self.socialite_instance = plugin.SocialitePlugin()
        user_ckan = self.socialite_instance.get_ckanuser(user_account)
        self.assertEqual(user_ckan['display_name'], 'Shani Agent')

if __name__ == '__main__':
    unittest.main(verbosity=2)