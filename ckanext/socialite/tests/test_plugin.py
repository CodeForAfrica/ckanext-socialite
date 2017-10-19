"""Tests for plugin.py."""
import collections
import unittest
from mock import MagicMock, patch
import ckan
from ckanext.socialite import plugin


class Session(object):
    """Mocking the Pylons Session Object
    """
    def __init__(self):
        self.collection = {}

    def __getitem__(self, key):
        return self.collection[key]

    def __setitem__(self, key, value):
        self.collection[key] = value

    def save(self):
        pass


class TestSocialitePlugin(unittest.TestCase):
    def setUp(self):
        """Create instances."""
        self.socialite_instance = plugin.SocialitePlugin()

    def tearDown(self):
        pass

    def test_update_config(self):
        """Test that CKAN uses the plugin's custom templates."""
        self._toolkit = plugin.toolkit
        plugin.toolkit = MagicMock()
        config = MagicMock()
        self.socialite_instance.update_config(config)
        plugin.toolkit.add_template_directory.assert_called_once_with(config, 'templates')
        plugin.toolkit = self._toolkit

    @patch('ckanext.socialite.plugin.pylons')
    @patch('ckanext.socialite.plugin.toolkit')
    @patch.object(plugin.SocialitePlugin, 'get_ckanuser')
    def test_login_when_user_exists(self, mock_get_ckanuser, mock_toolkit, mock_pylons):
        """Tests for successful login"""
        mock_get_ckanuser.return_value = {'name': 'Shani Agent'}
        mock_pylons.session = Session()
        mock_toolkit.request.params = dict([('name', 'Shani Agent'), ('email', 'buzzdhani@hotmail.com'), ('id_token', 'sPDwypON4z')])
        user_ckan = self.socialite_instance.login()
        self.assertEqual(mock_pylons.session.collection['ckanext_-user'], 'Shani Agent')
        self.assertEqual(mock_pylons.session.collection['ckanext_-email'], 'buzzdhani@hotmail.com')

    def get_mock_user(self):
        """Generate mock user for use during tests."""
        User = collections.namedtuple('User', 'display_name name email_hash id')
        return User(
            u'Shani Agent', u'dabelega',
            u'a18c6c1878ad16c5828240f5362c683e',
            u'fc91b5d4-7f39-47d6-a56e-cc122092fa95'
        )

    @patch.object(ckan.model.User, 'by_name')
    def test_get_ckanuser(self, mock_by_name):
        """Test CKAN user is retrieved by _getckanuser()."""
        self._toolkit = plugin.toolkit.get_action
        plugin.toolkit.get_action = MagicMock()

        mock_by_name.return_value = self.get_mock_user()
        ckan_user = self.socialite_instance.get_ckanuser('dabelega')
        self.assertEqual(plugin.toolkit.get_action()(), ckan_user)
        plugin.toolkit = self._toolkit

    def test_passwdcreation(self):
        """Test the CKAN password is created."""
        ckan_passwd = self.socialite_instance.get_ckanpasswd()
        self.assertIsNotNone(ckan_passwd)

if __name__ == '__main__':
    unittest.main(verbosity=2)
