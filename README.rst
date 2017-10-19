.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite.svg?branch=develop
    :target: https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite

.. image:: https://coveralls.io/repos/CodeForAfricaLabs/ckanext-socialite/badge.svg
  :target: https://coveralls.io/r/CodeForAfricaLabs/ckanext-socialite

.. image:: https://pypip.in/download/ckanext-socialite/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-socialite/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-socialite/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-socialite/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-socialite/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-socialite/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-socialite/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-socialite/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-socialite/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-socialite/
    :alt: License

=============
ckanext-socialite
=============

.. This extension allows a user to login to CKAN using their available social media accounts,
  that include Google, Github, LinkedIn and Facebook.
  <img width="1280" alt="screenshot ckan" src="https://user-images.githubusercontent.com/25458764/31724768-4d870d82-b42b-11e7-9859-08b310474bdd.png">


------------
Requirements
------------

This extension works perfectly with ckan v.2.6.3 to the v.2.7.0.
It is untested with v.2.8.0 going forward.

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-socialite:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-socialite Python package into your virtual environment::

     pip install ckanext-socialite

3. Add ``socialite`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------


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


------------------------
Development Installation
------------------------

To install ckanext-socialite for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/"andretalik"/ckanext-socialite.git
    cd ckanext-socialite
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    python -m pytest ckanext/socialite/tests/test_e2e

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    python -m pytest ckanext/socialite/tests/test_e2e --with-coverage

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.socialite --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-socialite on PyPI
---------------------------------

ckanext-socialite should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-socialite. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-socialite
----------------------------------------

ckanext-socialite is availabe on PyPI as https://pypi.python.org/pypi/ckanext-socialite.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
