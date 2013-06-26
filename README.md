# pyfacebook

An implementation of the Facebook graph API targeting ads.

Incomplete and in progress at the moment with more functionality to come.

## Development

### Python environment

When developing, it's helpful to work inside of a virtualenv.

If you have virtualenvwrapper installed you can create and work in one like so:

    mkvirtualenv pyfacebook
    workon pyfacebook

### Installation

Run setup script:

    python setup.py install

### Settings

Copy the settings file into place:

    cp pyfacebook/settings.py.default pyfacebook/settings.py

Fill in the appropriate values in `pyfacebook/settings.py`:

    FACEBOOK_APP_SECRET        = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    FACEBOOK_APP_ID            = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx='
    FACEBOOK_TEST_USERNAME     = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx='
    FACEBOOK_TEST_ACCOUNT_ID   = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx='
    FACEBOOK_PROD_ACCOUNT_ID   = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx='
    FACEBOOK_TEST_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx='

### Running tests

Install nose:

    pip install --upgrade nose

Run the tests:

    python setup.py nosetests
