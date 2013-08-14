from . import ApiTest
from mock import patch
from pyfacebook.api.aduser import AdUser


class TestAdUserApi(ApiTest):
    def setUp(self):
        super(TestAdUserApi, self).setUp(apis=[AdUser])

    def test_find_by_adaccount_id(self):
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdUser, number=2)):
            adusers = self.aduser_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID)
        for aduser in adusers:
            self.ok_(hasattr(aduser, 'role'))
            self.ok_(hasattr(aduser, 'id'))
