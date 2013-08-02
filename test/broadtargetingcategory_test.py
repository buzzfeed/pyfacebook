from . import ApiTest
from pyfacebook.api.broadtargetingcategory import BroadTargetingCategory


class TestBroadTargetingCategoryApi(ApiTest):
    def test_find_by_adaccount_id(self):
        btcs = BroadTargetingCategory(fb=self.fb).find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID)
        for btc in btcs:
            self.ok_(hasattr(btc, 'id'))
            self.ok_(hasattr(btc, 'name'))
            self.ok_(hasattr(btc, 'parent_category'))
            self.ok_(hasattr(btc, 'size'))
