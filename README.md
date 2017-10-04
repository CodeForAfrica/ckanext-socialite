# ckanext-socialite
[![Build Status](https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite.svg?branch=develop)](https://travis-ci.org/CodeForAfricaLabs/ckanext-socialite)
_[EXPERIMENTAL] A CKAN extension to allow login using Google, Facebook or Github._

It was noted that the CKAN Data Portal needed the new user to create a new account from within the product.
As a result, it was put forward that it should allow people to login using their social media accounts.
That is what this extension aims to achieve. It allows a new user to sign in using Google, Facebook, LinkedIn and Github.

## How It Works

This extension adds the relevant social media buttons to the login page allowing the user to login using them.

## Configuration

To use this extension with your own instance of Google Firebase,

```

```

## How to Install
------------
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
* That's All!
---

## License

MIT
