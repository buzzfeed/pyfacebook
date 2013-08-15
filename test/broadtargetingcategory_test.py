from . import ApiTest
from mock import patch
from pyfacebook.api.broadtargetingcategory import BroadTargetingCategory


class TestBroadTargetingCategoryApi(ApiTest):
    def setUp(self):
        super(TestBroadTargetingCategoryApi, self).setUp(apis=[BroadTargetingCategory])

    def test_find_by_adaccount_id(self):
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(BroadTargetingCategory, number=2)):
            btcs = self.broadtargetingcategory_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID)
        for btc in btcs:
            self.ok_(hasattr(btc, 'id'))
            self.ok_(hasattr(btc, 'name'))
            self.ok_(hasattr(btc, 'parent_category'))
            self.ok_(hasattr(btc, 'size'))
