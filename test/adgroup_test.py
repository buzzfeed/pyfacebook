from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID
from pyfacebook.settings import FACEBOOK_PROD_ACCOUNT_ID


from pyfacebook import PyFacebook

from nose.tools import eq_, ok_


class TestAdGroupApi():

    def setUp(self):
        self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                             access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                             app_secret=FACEBOOK_APP_SECRET)

    def test_find_by_adaccount_id(self):
        # Check order
        first_ten_adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=10, offset=0)
        second_five_adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=5, offset=5)

        eq_(len(first_ten_adgroups), 10)
        eq_(len(second_five_adgroups), 5)

        for c in first_ten_adgroups[5:]:
            index = first_ten_adgroups.index(c) - 5
            eq_(c.id, second_five_adgroups[index].id)

        # Check attributes
        adgroup = c
        ok_(not not adgroup.ad_id)
        ok_(not not adgroup.name)
        ok_(not not adgroup.campaign_id)
        ok_(not not adgroup.id)

        # Check completeness of paged results
        all_groups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID)
        for error in errors:
            print error.message
            print error.tb
        total = len(all_groups)

        limit = 3
        offset = total - limit + 1
        print "TOTAL:", total
        print "LIMIT:", limit
        print "OFFSET:", offset

        last_batch_of_groups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=limit, offset=offset)
        eq_(len(last_batch_of_groups), total - offset)

        # Check empty results
        no_groups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, offset=total)
        eq_(no_groups, [])

        # Check full results
        offset = 0
        all_groups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, offset=offset, limit=total + 1000)
        eq_(len(all_groups), total)

    def test_find_by_id(self):
        adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_TEST_ACCOUNT_ID)
        adgroup = adgroups[0]
        adgroup_by_id, errors = self.fb.api().adgroup().find_by_id(adgroup.id)

        eq_(adgroup.__dict__, adgroup_by_id.__dict__)

    def test_find_by_ids(self):
        base_adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_TEST_ACCOUNT_ID, limit=25)

        eq_(0, len(errors))

        # Test pulling 10 adgroups
        test_adgroup_ids = map(lambda x: x.id, base_adgroups)  # cool way of pulling a simple list of attributes from a list of more complex objects
        adgroups, errors = self.fb.api().adgroup().find_by_ids(test_adgroup_ids[:10])
        result_adgroup_ids = map(lambda x: x.id, adgroups)

        eq_(0, len(errors))
        eq_(10, len(adgroups))
        ok_(test_adgroup_ids[0] in result_adgroup_ids)

        # Test empty adgroup_ids error
        adgroups, errors = self.fb.api().adgroup().find_by_ids([])

        eq_(1, len(errors))
        eq_(errors[0].message, "A list of ids is required")
