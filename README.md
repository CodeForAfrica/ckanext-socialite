# ckanext-socialite
_[EXPERIMENTAL] A CKAN extension to allow login using Google, LinkedIn, Facebook or Github._

[![Build Status](https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite.svg?branch=develop)](https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite)


It was noted that the CKAN Data Portal needed the new user to create a new account from within the product.
As a result, it was put forward that it should allow people to login using their social media accounts.
That is what this extension aims to achieve. It allows a new user to sign in using Google, Facebook, LinkedIn and Github.

## How It Works

This extension adds the relevant social media buttons to the login page allowing the user to login using them.

## How to Install

Installing this extension in your CKAN instance is as easy as installing any other CKAN extension.

* Activate your virtual environment
```
. /usr/lib/ckan/default/bin/activate
```
* Install the extension
```
pip install ckanext-socialite
```
> **Note**: If you prefer, you can also download the source code and install the extension manually. To do so, execute the following commands:
> ```
> $ git clone https://github.com/CodeForAfricaLabs/ckanext-socialite.git
> $ cd ckanext-socialite
> $ python setup.py install
> ```

* Modify your configuration file (generally in `/etc/ckan/default/production.ini`) and add `socialite` in the `ckan.plugins` property.
```
ckan.plugins = <OTHER_PLUGINS> socialite
```

* Restart your apache2 reserver
```
sudo service apache2 restart
```
* Then correctly configure the extension through the instructions outlined below.

  The Configurations that have been marked as `OPTIONAL` do not need to be setup, rather those instructions outline how to configure the Authentication process with your own setups.


## Google Configuration

In your config file (/etc/ckan/default/production.ini) add these properties:

```
ckan.googleauth_clientid = client_id_value (REQUIRED). It contains the Client ID. For more information on how to create Client ID please visit https://developers.google.com/identity/sign-in/web/devconsole-project.
```
```
ckan.googleauth_hosted_domain = hosted_domain_value (OPTIONAL) It contains the domain authorized to authenticate. If it isn't set you will have access with any Google Account Credentials.
```

## Github Configuration(OPTIONAL)

To use this extension with your own instance of Google Firebase
Create a new Firebase project that you will use to host the login functionality of the extension.(https://console.firebase.google.com)

In the project setup, there shall be the config dictionary that you replace in the `ckanext/socialite/public/js/googleauth.js` file.

```
var config = {
  apiKey: 'apiKey',
  authDomain: 'authDomain',
  databaseURL: 'databaseURL',
  projectId: 'projectId',
  storageBucket: '',
  messagingSenderId: 'messagingSenderId'
}
```
On the Firebase console you then navigate to the Authentication tab and activate Github Authentication.

From the Sign-In methods tab, activate Github Login and copy the Client ID and Secret from Github and paste them into the required fields as shown in the screenshot.

<img width="1280" alt="screenshot ckan" src="https://user-images.githubusercontent.com/25458764/31397863-c827a8c2-adef-11e7-8a0c-90ebb432a934.png">

<img width="1280" alt="screenshot firebase" src="https://user-images.githubusercontent.com/25458764/31398089-7216c778-adf0-11e7-9e35-99ed1d2b3a44.png">

* That's all!

## Facebook Configuration(OPTIONAL)
*  Create your app on https://developers.facebook.com

*  Retrieve your app's API key from your dashboard.

*  In `ckanext/socialite/public/js/facebook.js`, set the value of `appId` to equal the APIKEY in step two. `appId` is located in the initialization function called `fbAsyncInit`.

## LinkedIn Configuration(OPTIONAL)
*  Create your app on https://developers.linkedin.com

*  Retrieve your app's API key from your dashboard.

*  In `ckanext/socialite/base.html`, set the value of api_key to equal the APIKEY retrieved in step two.

## Testing the Extension
This extension has tests for the backend functionality that is under CI on Travis-CI: https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite/

### End-to-End Tests
In order to run the E2E tests you must first of all download selenium's chromedriver from: https://sites.google.com/a/chromium.org/chromedriver/downloads
Extract to preferrably within the virtualenv to avoid Permission issues.

Then export the path to the chromedriver executable as an environment variable preferrably called "chromedriver_path"
```
export "chromedriver_path"=/usr/local/lib/ckan/default/bin/chromedriver
```
Afterwards run this code in your terminal once you are within the repo:
```
python -m pytest ckanext/socialite/tests/test_e2e/
```


### Plugin Backend Tests
To run the backend tests, simply cd into the repo root then run:
```
python -m pytest ckanext/socialite/tests/test_plugin.py
```


## License

MIT
