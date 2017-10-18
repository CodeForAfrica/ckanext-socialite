'''MIT License

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
SOFTWARE.'''


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
    return config.get('ckan.googleauth_clientid', '')

# get ckan.googleauth_hosted_domain from ini file
def get_hosted_domain():
    return config.get('ckan.googleauth_hosted_domain', '')


class AuthException(Exception):
    pass


class SocialitePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'googleauth')

    # declare new helper functions
    def get_helpers(self):
        return {'googleauth_get_clientid': get_google_clientid,
                'googleauth_get_hosted_domain': get_hosted_domain}

    # if exist returns ckan user
    def get_ckanuser(self, user):
        import ckan.model

        user_ckan = ckan.model.User.by_name(user)

        if user_ckan:
            user_dict = toolkit.get_action('user_show')(data_dict={'id': user_ckan.id})
            return user_dict
        else:
            return None

    # generates a strong password
    def get_ckanpasswd(self):
        import datetime
        import random
        passwd = str(random.random()) + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+str(uuid.uuid4().hex)
        passwd = re.sub(r"\s+", "", passwd, flags=re.UNICODE)
        return passwd

    def _logout_user(self):
        #import pylons
        # to revoke the Google token uncomment the code below
        #if 'ckanext_-accesstoken' in pylons.session:
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


    #at every access the email address is checked. if it is authorized ckan username is created and access is given
    def login(self):

        params = toolkit.request.params
        if 'id_token' in params:
            user_account = params['email'].split('@')[0]
            full_name = params['name']
            user_email = params['email']
            if user_account.isalnum() is False:
                user_account = ''.join(e for e in user_account if e.isalnum())

            user_ckan = self.get_ckanuser(user_account)
            
            if not user_ckan:
                print(params['email'], 'the after email')
                user_ckan = toolkit.get_action('user_create')(
                                        context={'ignore_auth': True},
                                        data_dict={'email': user_email,
                                            'name': user_account,
                                            'fullname': full_name,
                                            'password': self.get_ckanpasswd()})

            pylons.session['ckanext_-user'] = user_ckan['name']
            pylons.session['ckanext_-email'] = user_email
            pylons.session.save()

    #if someone is logged in will be set the parameter c.user
    def identify(self):
        user_ckan = pylons.session.get('ckanext_-user')
        if user_ckan:
            toolkit.c.user = user_ckan

    def logout(self):
        self._logout_user()

    def abort(self):
        self._logout_user()
