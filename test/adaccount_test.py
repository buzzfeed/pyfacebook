from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID

from pyfacebook import PyFacebook

from nose.tools import eq_, ok_

class TestAdAccountApi( ):
  def setUp(self):
    self.fb = PyFacebook( app_id=FACEBOOK_APP_ID,
                          access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                          app_secret=FACEBOOK_APP_SECRET )

  def test_find_by_id(self):
    adaccount, errors = self.fb.api().adaccount().find_by_id( 'act_' + str( FACEBOOK_TEST_ACCOUNT_ID ) ) # Buzzfeed account id
    ok_( not errors )
    eq_( adaccount.name, u'BuzzFeed RnD_API Testing' )
    eq_( adaccount.account_status, 1 )
    eq_( adaccount.id, u'act_' + str( FACEBOOK_TEST_ACCOUNT_ID ) )
    eq_( adaccount.timezone_name, u'America/Los_Angeles' )
    eq_( adaccount.currency, u'USD' )
    eq_( str(adaccount.account_id), str(FACEBOOK_TEST_ACCOUNT_ID) )
