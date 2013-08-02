from . import ApiTest
from pyfacebook.api.aduser import AdUser


class TestAdUserApi(ApiTest):
    def test_find_by_adaccount_id(self):
        adusers = AdUser(fb=self.fb).find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID)
        for aduser in adusers:
            self.ok_(hasattr(aduser, 'role'))
            self.ok_(hasattr(aduser, 'id'))
