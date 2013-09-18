import unittest
from nose.tools import ok_, eq_
from pyfacebook import settings
from pyfacebook import PyFacebook


class InternalsTest(unittest.TestCase):

    def test_validate_access_token(self):
        app_id = settings.__dict__.get('FACEBOOK_APP_ID')
        app_secret = settings.__dict__.get('FACEBOOK_APP_SECRET')
        test_token_text = settings.__dict__.get('FACEBOOK_TEST_ACCESS_TOKEN')
        if app_id and app_secret and test_token_text:
            pyfb = PyFacebook(app_id=app_id, app_secret=app_secret, token_text=test_token_text)
            ok_(pyfb.access_token)
