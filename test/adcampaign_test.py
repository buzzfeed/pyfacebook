from nose.tools import eq_, ok_
from pyfacebook import PyFacebook

from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_PROD_ACCOUNT_ID

class TestAdCampaignApi():
  def setUp(self):
    self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                         access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                         app_secret=FACEBOOK_APP_SECRET)

  def test_find_by_adaccount_id(self):
    adcampaigns, errors = self.fb.api().adcampaign().find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, limit=2, offset=2 )

    eq_( 0, len( errors ) )
    eq_( 2, len( adcampaigns ) )

    adcampaign          = adcampaigns[ 0 ]

    ok_( not not adcampaign.id )
    ok_( not not adcampaign.account_id )
    ok_( not not adcampaign.name )

  def test_find_by_adgroup_id_and_find_by_id(self):
    adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=2)
    adgroup = adgroups[0]

    adcampaign, errors = self.fb.api().adcampaign().find_by_adgroup_id(adgroup.id)
    adcampaign_by_id, errors = self.fb.api().adcampaign().find_by_id(adgroup.campaign_id)
    eq_(str(adcampaign.id), adcampaign_by_id.id)
    eq_(str(adcampaign.account_id), FACEBOOK_PROD_ACCOUNT_ID)
    eq_(str(adcampaign.end_time), adcampaign_by_id.end_time)
    eq_(str(adcampaign.name), adcampaign_by_id.name)

  def test_find_by_ids( self ):
    base_adcampaigns, errors = self.fb.api( ).adcampaign( ).find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, limit=25 )

    eq_( 0, len( errors ) )

    #Test pulling 10 adcampaigns
    test_adcampaign_ids      = map( lambda x: x.id, base_adcampaigns ) #cool way of pulling a simple list of attributes from a list of more complex objects
    adcampaigns, errors      = self.fb.api( ).adcampaign( ).find_by_ids( test_adcampaign_ids[:10] )
    result_adcampaign_ids      = map( lambda x: x.id, adcampaigns )

    eq_( 0, len( errors ) )
    eq_( 10, len( adcampaigns ) )
    ok_( test_adcampaign_ids[0] in result_adcampaign_ids )

    #Test empty adcampaign_ids error
    adcampaigns, errors = self.fb.api( ).adcampaign( ).find_by_ids( [ ] )

    eq_( 1, len( errors ) )
    eq_( errors[ 0 ].message, "A list of ids is required" )
