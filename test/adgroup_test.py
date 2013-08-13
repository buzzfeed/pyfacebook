from . import ApiTest
from pyfacebook.api.adgroup import AdGroup


class TestAdGroupApi(ApiTest):

    def setUp(self):
        super(TestAdGroupApi, self).setUp(apis=[AdGroup])

    def test_find_by_adaccount_id(self):
        # Check order
        first_ten_adgroups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, limit=10, offset=0)
        second_five_adgroups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, limit=5, offset=5)

        self.eq_(len(first_ten_adgroups), 10)
        self.eq_(len(second_five_adgroups), 5)

        for c in first_ten_adgroups[5:]:
            index = first_ten_adgroups.index(c) - 5
            self.eq_(c.id, second_five_adgroups[index].id)

        # Check attributes
        adgroup = c
        self.ok_(not not adgroup.name)
        self.ok_(not not adgroup.campaign_id)
        self.ok_(not not adgroup.id)

        # Check completeness of paged results
        all_groups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID)
        total = len(all_groups)

        limit = 3
        offset = total - limit + 1

        last_batch_of_groups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, limit=limit, offset=offset)
        self.eq_(len(last_batch_of_groups), total - offset)

        # Check empty results
        no_groups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, offset=total)
        self.eq_(no_groups, [])

        # Check full results
        offset = 0
        all_groups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, offset=offset, limit=total + 1000)
        self.eq_(len(all_groups), total)

    def test_find_by_id(self):
        adgroups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID)
        adgroup = adgroups[0]
        adgroup_by_id = self.adgroup_api.find_by_id(adgroup.id)

        self.eq_(adgroup.to_json(return_dict=True), adgroup_by_id.to_json(return_dict=True))

    def test_find_by_ids(self):
        base_adgroups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, limit=25)

        # Test pulling 10 adgroups
        test_adgroup_ids = map(lambda x: x.id, base_adgroups)  # cool way of pulling a simple list of attributes from a list of more complex objects
        adgroups = self.adgroup_api.find_by_ids(test_adgroup_ids[:10])
        result_adgroup_ids = map(lambda x: x.id, adgroups)

        self.eq_(10, len(adgroups))
        self.ok_(test_adgroup_ids[0] in result_adgroup_ids)

        # Test empty adgroup_ids error
        try:
            adgroups = self.adgroup_api.find_by_ids([])
        except Exception, e:
            self.eq_(e.message, "A list of ids is required")
