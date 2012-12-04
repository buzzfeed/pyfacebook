from datetime import datetime
from nose.tools import eq_
from pyfacebook import PyFacebook

from discotech.api import (
    social_ad_campaign,
    social_ad_family,
    social_ad_run,
    social_ad
)

from django.utils.timezone import utc
from discotech.models import Vendor, SocialAdCampaign
from discotech.settings import FACEBOOK_APP_SECRET
from discotech.settings import FACEBOOK_APP_ID
from discotech.settings import FACEBOOK_TEST_ACCESS_TOKEN
from discotech.settings import FACEBOOK_TEST_ACCOUNT_ID


class TestAdCampaignApi():
    def setUp(self):
        self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                             access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                             app_secret=FACEBOOK_APP_SECRET)

    def test_find_by_adgroup_id_and_find_by_id(self):
        adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_TEST_ACCOUNT_ID)
        adgroup = adgroups[0]

        adcampaign, errors = self.fb.api().adcampaign().find_by_adgroup_id(adgroup.id)
        adcampaign_by_id, errors = self.fb.api().adcampaign().find_by_id(adgroup.campaign_id)
        eq_(str(adcampaign.id), adcampaign_by_id.id)
        eq_(str(adcampaign.account_id), FACEBOOK_TEST_ACCOUNT_ID)
        eq_(str(adcampaign.end_time), adcampaign_by_id.end_time)
        eq_(str(adcampaign.name), adcampaign_by_id.name)

    def test_get_active(self):
        active_campaigns, errs = social_ad_campaign.get_active()
        eq_(len(active_campaigns), 0)  # there should be nothing yet

        adcampaign, errs = social_ad_campaign.get_or_create('test_campaign', 0)
        adfamily, errs = social_ad_family.create(adcampaign, 'http://somelink.com', 0)
        # some dummy data for having the relationship with SocialAd
        vendor = Vendor.objects.create(title='test', display_name='Test')
        title, body, image, vendor_product, buzzfeed_product, segment = [None] * 6
        vendor_ad_id = ''
        vendor_ad_status, vendor_bid_type, vendor_max_bid, budget = [1] * 4
        tracking_hash = 'test'
        ad, errs = social_ad.create(adfamily, vendor, title, body, image,
                              vendor_product, buzzfeed_product, segment,
                              vendor_ad_id, vendor_ad_status, vendor_bid_type,
                              vendor_max_bid, budget, tracking_hash)
        # have an AdRun to be found
        now = datetime.now().date()
        started_at = datetime(year=now.year - 1, month=1, day=1, tzinfo=utc)
        finished_at = datetime(year=now.year + 1, month=1, day=1, tzinfo=utc)
        social_ad_run.create(ad, started_at, finished_at)
        # check for active campaigns
        active_campaigns, errors = social_ad_campaign.get_active()
        eq_(len(active_campaigns), 1)
