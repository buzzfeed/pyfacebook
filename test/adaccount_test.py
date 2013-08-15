from . import ApiTest
from mock import patch
from pyfacebook.api.adaccount import AdAccount


class TestAdAccountApi(ApiTest):
    def setUp(self):
        super(TestAdAccountApi, self).setUp(apis=[AdAccount])

    def test_find_by_id(self):
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdAccount)):
            adaccount = self.adaccount_api.find_by_id('act_' + str(self.FACEBOOK_TEST_ACCOUNT_ID))  # Buzzfeed account id
            self.eq_(adaccount.name, u'BuzzFeed RnD_API Testing')
            self.eq_(adaccount.account_status, 1)
            self.eq_(adaccount.id, u'act_' + str(self.FACEBOOK_TEST_ACCOUNT_ID))
            self.eq_(adaccount.timezone_name, u'America/Los_Angeles')
            self.eq_(adaccount.currency, u'USD')
            self.eq_(str(adaccount.account_id), str(self.FACEBOOK_TEST_ACCOUNT_ID))
