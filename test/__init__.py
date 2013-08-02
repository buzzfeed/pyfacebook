from caliendo.facade import Facade
from nose.tools import eq_, ok_, set_trace
from pyfacebook import PyFacebook
from pyfacebook.settings import (
    FACEBOOK_APP_SECRET,
    FACEBOOK_APP_ID,
    FACEBOOK_TEST_ACCESS_TOKEN,
    FACEBOOK_PROD_ACCOUNT_ID,
    FACEBOOK_TEST_ACCOUNT_ID
)

class ApiTest(object):
    def __init__(self, *args, **kwargs):
        self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                             access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                             app_secret=FACEBOOK_APP_SECRET)
        super(ApiTest, self).__init__(*args, **kwargs)
        self.ok_ = ok_
        self.eq_ = eq_
        self.set_trace = set_trace
        self.FACEBOOK_PROD_ACCOUNT_ID = FACEBOOK_PROD_ACCOUNT_ID
        self.FACEBOOK_TEST_ACCOUNT_ID = FACEBOOK_TEST_ACCOUNT_ID

    def setUp(self, apis=[], facade=False):
        for api_ in apis:
            api_name = api_.__name__.lower() + '_api'
            if facade:
                setattr(self, api_name, Facade(api_(fb=self.fb)))
            else:
                setattr(self, api_name, api_(fb=self.fb))
