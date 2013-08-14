import datetime
from mock import patch
import pytz
from . import ApiTest
from pyfacebook.api.adgroup import AdGroup
from pyfacebook.api.adstatistic import AdStatistic


class TestAdStatisticApi(ApiTest):
    def setUp(self):
        super(TestAdStatisticApi, self).setUp(apis=[AdStatistic, AdGroup])

    def one_percent_more(self, somevalue):
        return somevalue + 0.01 * somevalue

    def one_percent_less(self, somevalue):
        return somevalue - 0.01 * somevalue

    def test_find_by_adaccount_id_and_find_by_adgroup_ids(self):
        include_deleted = True
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdGroup, number=2)):
            adgroups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_TEST_ACCOUNT_ID, include_deleted=include_deleted)
        all_stats = {
            'social_unique_clicks': 0,
            'unique_impressions': 0,
            'social_clicks': 0,
            'social_impressions': 0,
            'social_unique_impressions': 0,
            'social_spent': 0,
            'impressions': 0,
            'clicks': 0,
            'unique_clicks': 0,
        }

        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdStatistic, number=2)):
            stats = self.adstatistic_api.find_by_adgroup_ids([adgroup.id for adgroup in adgroups], self.FACEBOOK_PROD_ACCOUNT_ID, include_deleted=include_deleted)
        for stat in stats:
            for key, val in all_stats.items():
                addtl_val = None
                if hasattr(stat, key):
                    addtl_val = getattr(stat, key)
                if addtl_val:
                    all_stats[key] = val + int(addtl_val)

        totals = {
            'social_unique_clicks': 492,
            'social_impressions': 49380,
            'social_clicks': 49382712,
            'unique_impressions': 4936,
            'social_unique_impressions': 8,
            'social_spent': 3200,
            'impressions': 4000,
            'clicks': 4,
            'unique_clicks': 493824,
        }
        for key, val in all_stats.items():
            if val:  # if val=0, the stat has no activity for the current account
                to_compare = totals[key]
                self.ok_(val > self.one_percent_less(to_compare) or val == int(to_compare))
                self.ok_(val < self.one_percent_more(to_compare) or val == int(to_compare))

    def test_find_by_start_time_end_time(self):
        utc = pytz.utc
        # Test single day
        start_time = datetime.datetime(2012, 12, 26, 6, 0, 0, tzinfo=utc)
        end_time = datetime.datetime(2012, 12, 27, 6, 0, 0, tzinfo=utc)
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdStatistic, number=2)):
            stats = self.adstatistic_api.find_by_start_time_end_time(self.FACEBOOK_PROD_ACCOUNT_ID, start_time, end_time)
            self.ok_(len(stats) > 0)

        # Test one month: paging
        start_time = datetime.datetime(2012, 11, 26, 6, 0, 0, tzinfo=utc)
        end_time = datetime.datetime(2012, 12, 27, 6, 0, 0, tzinfo=utc)
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdStatistic, number=2)):
            stats = self.adstatistic_api.find_by_start_time_end_time(self.FACEBOOK_PROD_ACCOUNT_ID, start_time, end_time)
            self.ok_(len(stats) > 0)
