from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID

from pyfacebook import PyFacebook

from nose.tools import eq_, ok_

class TestAdGroupApi( ):

  def setUp(self):
    self.fb = PyFacebook( app_id=FACEBOOK_APP_ID,
                          access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                          app_secret=FACEBOOK_APP_SECRET )

  def test_find_by_adaccount_id(self):
    adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID, limit=2, offset=2 )

    eq_( 0, len( errors ) )
    eq_( 2, len( adgroups ) )
    adgroup          = adgroups[0]

    ok_( not not adgroup.ad_id )
    ok_( not not adgroup.name )
    ok_( not not adgroup.campaign_id )
    ok_( not not adgroup.id )

  def test_find_by_id(self):
    adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID )
    adgroup          = adgroups[0]
    adgroup_by_id, errors = self.fb.api().adgroup().find_by_id( adgroup.id )

    eq_( adgroup.__dict__, adgroup_by_id.__dict__ )

  def test_find_by_ids( self ):
    base_adgroups, errors = self.fb.api( ).adgroup( ).find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID, limit=25 )

    eq_( 0, len( errors ) )

    #Test pulling 10 adgroups
    test_adgroup_ids      = map( lambda x: x.id, base_adgroups ) #cool way of pulling a simple list of attributes from a list of more complex objects
    adgroups, errors      = self.fb.api( ).adgroup( ).find_by_ids( test_adgroup_ids[:10] )
    result_adgroup_ids    = map( lambda x: x.id, adgroups )

    eq_( 0, len( errors ) )
    eq_( 10, len( adgroups ) )
    ok_( test_adgroup_ids[0] in result_adgroup_ids )

    #Test empty adgroup_ids error
    adgroups, errors = self.fb.api( ).adgroup( ).find_by_ids( [ ] )

    eq_( 1, len( errors ) )
    eq_( errors[ 0 ].message, "A list of ids is required" )
