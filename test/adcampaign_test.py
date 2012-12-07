from nose.tools import eq_
from pyfacebook import PyFacebook

from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID


class TestAdCampaignApi():
    def setUp(self):
        self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                             access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                             app_secret=FACEBOOK_APP_SECRET)

    def test_find_by_adgroup_id_and_find_by_id(self):
        adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_TEST_ACCOUNT_ID)

        if errors:
          for err in errors:
            print err.message

        adgroup = adgroups[0]

        adcampaign, errors = self.fb.api().adcampaign().find_by_adgroup_id(adgroup.id)
        adcampaign_by_id, errors = self.fb.api().adcampaign().find_by_id(adgroup.campaign_id)
        eq_(str(adcampaign.id), adcampaign_by_id.id)
        eq_(str(adcampaign.account_id), FACEBOOK_TEST_ACCOUNT_ID)
        eq_(str(adcampaign.end_time), adcampaign_by_id.end_time)
        eq_(str(adcampaign.name), adcampaign_by_id.name)