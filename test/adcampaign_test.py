from . import ApiTest
from mock import patch
from pyfacebook.api.adcampaign import AdCampaign
from pyfacebook.api.adgroup import AdGroup


class TestAdCampaignApi(ApiTest):
    def setUp(self):
        super(TestAdCampaignApi, self).setUp(apis=[AdCampaign, AdGroup])

    def test_find_by_adaccount_id(self):
        # Check order
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdCampaign, number=10)):
            first_ten_adcampaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=10, offset=0)
            second_five_adcampaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=5, offset=5)
            self.eq_(len(first_ten_adcampaigns), 10)
            self.eq_(len(second_five_adcampaigns), 5)

            for c in first_ten_adcampaigns[5:]:
                index = first_ten_adcampaigns.index(c) - 5
                self.eq_(c.id, second_five_adcampaigns[index].id)

            # Check attributes
            adcampaign = first_ten_adcampaigns[-1]
            self.ok_(not not adcampaign.id)
            self.eq_(adcampaign.account_id, int(self.FACEBOOK_PROD_ACCOUNT_ID))
            self.ok_(not not adcampaign.name)

            # Check completeness of paged results
            all_campaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID)
            total = len(all_campaigns)
            limit = 3
            offset = total - limit + 1
            if offset < 0:  # facebook api does not support negative offsets
                offset = 0
            last_batch_of_campaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=limit, offset=offset)
            self.eq_(len(last_batch_of_campaigns), total - offset)

            # Check empty results
            no_campaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, offset=total)
            self.eq_(no_campaigns, [])

            # Check full results
            all_campaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, offset=0, limit=total+1000)
            self.eq_(len(all_campaigns), total)

    def test_find_by_adgroup_id_and_find_by_id(self):
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdGroup, number=2)):
            adgroups = self.adgroup_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=2)
            adgroup = adgroups[0]

        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdCampaign)):
            with patch('pyfacebook.api.adgroup.AdGroup.find_by_id', **{'return_value': adgroup}):
                adcampaign = self.adcampaign_api.find_by_adgroup_id(adgroup.id)
            adcampaign_by_id = self.adcampaign_api.find_by_id(adgroup.campaign_id)
            self.eq_(adcampaign.id, adcampaign_by_id.id)
            self.eq_(str(adcampaign.account_id), self.FACEBOOK_PROD_ACCOUNT_ID)
            self.eq_(str(adcampaign.end_time), adcampaign_by_id.end_time)
            self.eq_(str(adcampaign.name), adcampaign_by_id.name)

    def test_find_by_ids(self):
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdCampaign, number=25)):
            base_adcampaigns = self.adcampaign_api.find_by_adaccount_id(self.FACEBOOK_PROD_ACCOUNT_ID, limit=25)

        #Test pulling 10 adcampaigns
        test_adcampaign_ids = map(lambda x: x.id, base_adcampaigns)[:10]
        with patch('pyfacebook.PyFacebook._json_response',
                   **self.get_patch_kwargs(AdCampaign, number=len(test_adcampaign_ids), nest_by_id=True)):
            adcampaigns = self.adcampaign_api.find_by_ids(test_adcampaign_ids)
            result_adcampaign_ids = map(lambda x: x.id, adcampaigns)

            self.eq_(len(test_adcampaign_ids), len(adcampaigns))
            self.ok_(test_adcampaign_ids[0] in result_adcampaign_ids)

        #Test empty adcampaign_ids error
        with patch('pyfacebook.PyFacebook._json_response', **self.get_patch_kwargs(AdCampaign, number=0, nest_by_id=True)):
            try:
                adcampaigns = self.adcampaign_api.find_by_ids([])
            except Exception, e:
                self.eq_(e.message, "A list of ids is required")
