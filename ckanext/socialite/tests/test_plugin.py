"""Tests for plugin.py."""
import collections
import unittest
from mock import MagicMock, patch
import ckan
from ckanext.socialite import plugin
from collections import defaultdict


class Session(dict):
    """Mocking the Pylons Session Object."""
    def __init__(self):
        self['ckanext_user'] = 'buzzdhani'
        self['ckanext_email'] = 'buzzdhani@hotmail.com'

    def save(self):
        pass


class TestSocialitePlugin(unittest.TestCase):
    """This class holds the TestCase instance through which all tests are done."""
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
        self.assertEqual(mock_pylons.session['ckanext_user'], 'Shani Agent')
        self.assertEqual(mock_pylons.session['ckanext_email'], 'buzzdhani@hotmail.com')

    @patch('ckanext.socialite.plugin.pylons')
    @patch('ckanext.socialite.plugin.toolkit.get_action')
    @patch('ckanext.socialite.plugin.toolkit')
    @patch.object(plugin.SocialitePlugin, 'get_ckanuser')
    def test_new_login(self, mock_get_ckanuser, mock_toolkit, mock_get_action, mock_pylons):
        """Tests for successful new login."""
        mock_get_ckanuser.return_value = None
        mock_pylons.session = Session()
        mock_toolkit.request.params = dict([('name', 'Shani Agent'), ('email', 'buzzdhani@hotmail.com'), ('id_token', 'sPDwypON4z')])
        user_dict = {'email': 'buzzdhani@hotmail.com',
                     'name': 'buzzdhani',
                     'full_name': 'Shani Agent',
                     'password': 'nfnfndndndh'}
        mock_get_action.return_value = lambda context, data_dict: user_dict
        user_account = mock_toolkit.request.params['email'].split('@')[0]
        full_name = mock_toolkit.request.params['name']
        user_email = mock_toolkit.request.params['email']
        user_ckan = self.socialite_instance.login()
        self.assertEqual(mock_pylons.session['ckanext_user'], 'buzzdhani')
        self.assertEqual(mock_pylons.session['ckanext_email'], 'buzzdhani@hotmail.com')

    def get_mock_user(self):
        """Generate mock user for use during tests."""
        User = collections.namedtuple('User', 'display_name name email_hash id')
        return User(
            u'Shani Agent', u'dabelega',
            u'a18c6c1878ad16c5828240f5362c683e',
            u'fc91b5d4-7f39-47d6-a56e-cc122092fa95'
        )

    @patch.object(ckan.model.User, 'by_name')
    @patch('ckanext.socialite.plugin.toolkit.get_action')
    def test_get_ckanuser(self, mock_get_action, mock_by_name):
        """Test CKAN user is retrieved with correct credentials."""
        user_dict = {'email': 'buzzdhani@hotmail.com',
                     'name': 'buzzdhani',
                     'full_name': 'Shani Agent'}
        mock_get_action.return_value = lambda data_dict: user_dict

        user_ckan = self.socialite_instance.get_ckanuser('nhggfdretee')
        self.assertEqual(user_ckan, user_dict)

    def test_passwdcreation(self):
        """Test the CKAN password is created."""
        ckan_passwd = self.socialite_instance.get_ckanpasswd()
        self.assertIsNotNone(ckan_passwd)

    @patch('ckanext.socialite.plugin.pylons')
    def test_logout(self, mock_pylons):
        """Test CKAN user is logged out."""
        mock_pylons.session = Session()
        self.socialite_instance._logout_user()
        self.assertEqual(mock_pylons.session.get('ckanext_email'), None)
        self.assertEqual(mock_pylons.session.get('ckanext_user'), None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
