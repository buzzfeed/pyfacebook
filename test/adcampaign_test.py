from nose.tools import eq_, ok_
from caliendo.facade import Facade
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
    adcampaign_api = Facade(self.fb.api().adcampaign())
    # Check order
    first_ten_adcampaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, limit=10, offset=0 )
    second_five_adcampaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, limit=5, offset=5 )
    eq_( len( first_ten_adcampaigns ), 10 )
    eq_( len( second_five_adcampaigns ), 5 )

    for c in first_ten_adcampaigns[5:]:
        index = first_ten_adcampaigns.index(c) - 5
        eq_( c.id, second_five_adcampaigns[index].id )

    # Check attributes
    adcampaign = first_ten_adcampaigns[-1]
    ok_( not not adcampaign.id )
    eq_( adcampaign.account_id, int(FACEBOOK_PROD_ACCOUNT_ID) )
    ok_( not not adcampaign.name )

    # Check completeness of paged results
    all_campaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID )
    total = len(all_campaigns)
    limit = 3
    offset = total - limit + 1
    if offset < 0:  # facebook api does not support negative offsets
            offset = 0
    last_batch_of_campaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, limit=limit, offset=offset )
    eq_( len(last_batch_of_campaigns), total - offset )

    # Check empty results
    no_campaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, offset=total )
    eq_( no_campaigns, [] )

    # Check full results
    all_campaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, offset=0, limit=total+1000)
    eq_( len(all_campaigns), total )


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
    adcampaign_api = Facade(self.fb.api().adcampaign())
    base_adcampaigns, errors = adcampaign_api.find_by_adaccount_id( FACEBOOK_PROD_ACCOUNT_ID, limit=25 )
    eq_( 0, len( errors ) )

    #Test pulling 10 adcampaigns
    test_adcampaign_ids      = map( lambda x: x.id, base_adcampaigns )[:10] #cool way of pulling a simple list of attributes from a list of more complex objects
    adcampaigns, errors      = adcampaign_api.find_by_ids( test_adcampaign_ids )
    result_adcampaign_ids      = map( lambda x: x.id, adcampaigns )

    eq_( 0, len( errors ) )
    eq_( len(test_adcampaign_ids), len( adcampaigns ) )
    ok_( test_adcampaign_ids[0] in result_adcampaign_ids )

    #Test empty adcampaign_ids error
    adcampaigns, errors = adcampaign_api.find_by_ids( [ ] )

    eq_( 1, len( errors ) )
    eq_( errors[ 0 ].message, "A list of ids is required" )
