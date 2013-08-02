from . import ApiTest
from pyfacebook.api.adgroup import AdGroup
from pyfacebook.api.adcreative import AdCreative


class TestAdCreativeApi(ApiTest):

    def setUp(self):
        super(TestAdCreativeApi, self).setUp(apis=[AdCreative])

    def test_find_by_adaccount_id(self):
        # Check order
        first_ten_adcreatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=10, offset=0)
        second_five_adcreatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=5, offset=5)

        self.eq_(len(first_ten_adcreatives), 10)
        self.eq_(len(second_five_adcreatives), 5)

        for c in first_ten_adcreatives[5:]:
            index = first_ten_adcreatives.index(c) - 5
            self.eq_(c.id, second_five_adcreatives[index].id)

        # Check attributes
        adcreative = c
        self.ok_(not not adcreative.body)
        self.ok_(not not adcreative.name)
        self.ok_(not not adcreative.link_url)
        self.ok_(not not adcreative.title)

        # Check completeness of paged results
        all_creatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID)
        total = len(all_creatives)

        limit = 3
        offset = total - limit + 1
        last_batch_of_creatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=limit, offset=offset)
        self.eq_(len(last_batch_of_creatives), total - offset)

        # Check empty results
        no_creatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, offset=total)
        self.eq_(no_creatives, [])

        # Check full results
        offset = 0
        all_creatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, offset=offset, limit=total + 1000)
        self.eq_(len(all_creatives), total)

    def test_find_by_adgroup_id(self):
        adgroups = AdGroup(fb=self.fb).find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, limit=2)
        adgroup = adgroups[0]

        adcreatives = self.adcreative_api.find_by_adgroup_id(adgroup.id)
        adcreative = adcreatives[0]

        self.ok_(not not adcreative.name)
        self.ok_(not not adcreative.type)
        self.ok_(not not adcreative.action_spec)

    def test_find_by_ids(self):
        base_adcreatives = self.adcreative_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, limit=25)

        # Test pulling 10 adcreatives
        test_adcreative_ids = map(lambda x: x.id, base_adcreatives)  # cool way of pulling a simple list of attributes from a list of more complex objects
        adcreatives = self.adcreative_api.find_by_ids(test_adcreative_ids[:10])
        result_adcreative_ids = map(lambda x: x.id, adcreatives)

        self.eq_(10, len(adcreatives))
        self.ok_(test_adcreative_ids[0] in result_adcreative_ids)

        # Test empty adcreative_ids error
        try:
            adcreatives = self.adcreative_api.find_by_ids([])
        except Exception, e:
            self.eq_(e.message, "A list of ids is required")
