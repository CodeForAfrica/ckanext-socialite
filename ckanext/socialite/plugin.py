"""MIT License.

Copyright (c) 2017 Code for Africa - LABS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# coding=utf-8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import json
import uuid
import pylons
import pylons.config as config
import ckan.lib.helpers as helpers
import requests
import re
import logging


# get 'ckan.googleauth_clientid' from ini file
def get_google_clientid():
    """Extract Client ID from config file."""
    return config.get('ckan.googleauth_clientid', '')


# get ckan.googleauth_hosted_domain from ini file
def get_hosted_domain():
    """Extract Hosted Domain from config file."""
    return config.get('ckan.googleauth_hosted_domain', '')


class AuthException(Exception):
    """Exception to be raised for errors."""

    pass


class SocialitePlugin(plugins.SingletonPlugin):
    """Set up plugin for CKAN integration."""

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config_):
        """Add resources used by the plugin into core config file."""
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'googleauth')

    def get_helpers(self):
        """Declare new helper functions."""
        return {'googleauth_get_clientid': get_google_clientid,
                'googleauth_get_hosted_domain': get_hosted_domain}

    def get_ckanuser(self, user):
        """Return CKAN user if it already exists."""
        #import pdb; pdb.set_trace()
        import ckan.model

        user_ckan = ckan.model.User.by_name(user)

        if user_ckan:
            #import pdb; pdb.set_trace()
            user_dict = toolkit.get_action('user_show')(data_dict={'id': user_ckan.id})
            return user_dict
        else:
            return None

    def get_ckanpasswd(self):
        """Generate strong password for CKAN user."""
        import datetime
        import random
        passwd = str(random.random()) + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+str(uuid.uuid4().hex)
        passwd = re.sub(r"\s+", "", passwd, flags=re.UNICODE)
        return passwd

    def _logout_user(self):
        """Log out the currently logged in CKAN user."""
        # import pylons
        # to revoke the Google token uncomment the code below
        # if 'ckanext_-accesstoken' in pylons.session:
        #    atoken = pylons.session.get('ckanext_-accesstoken')
        #    res = requests.get('https://accounts.google.com/o/oauth2/revoke?token='+atoken)
        #    if res.status_code == 200:
        #       del pylons.session['ckanext_-accesstoken']
        #    else:
        #   raise GoogleAuthException('Token not revoked')
        if 'ckanext_-user' in pylons.session:
            del pylons.session['ckanext_-user']
        if 'ckanext_-email' in pylons.session:
            del pylons.session['ckanext_-email']
        pylons.session.save()

    def login(self):
        """Login the user with credentials from the SocialAuth used. The CKAN
        username is created and access given.
        """
        params = toolkit.request.params
        if 'id_token' in params:
            user_account = params['email'].split('@')[0]
            full_name = params['name']
            user_email = params['email']
            if user_account.isalnum() is False:
                user_account = ''.join(e for e in user_account if e.isalnum())

            user_ckan = self.get_ckanuser(user_account)

            if not user_ckan:
                user_ckan = toolkit.get_action('user_create')(
                                        context={'ignore_auth': True},
                                        data_dict={'email': user_email,
                                                   'name': user_account,
                                                   'fullname': full_name,
                                                   'password': self.get_ckanpasswd()})

            pylons.session['ckanext_-user'] = user_ckan['name']
            pylons.session['ckanext_-email'] = user_email
            pylons.session.save()

    # if someone is logged in will be set the parameter c.user
    def identify(self):
        """Logged in CKAN user will be set as c.user parameter."""
        user_ckan = pylons.session.get('ckanext_-user')
        if user_ckan:
            toolkit.c.user = user_ckan

    def logout(self):
        """Call _logout_user()."""
        self._logout_user()

    def abort(self):
        """In case of any errors, calls _logout_user()."""
        self._logout_user()
