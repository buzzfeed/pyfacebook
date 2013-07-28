from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID

from pyfacebook import PyFacebook

from nose.tools import ok_

class TestAdUserApi( ):

  def test_find_by_adaccount_id(self):
    fb = PyFacebook( app_id=FACEBOOK_APP_ID,
                     access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                     app_secret=FACEBOOK_APP_SECRET )

    adusers = fb.api().aduser().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID )

    for aduser in adusers:
      ok_( hasattr( aduser, 'role' ) )
      ok_( hasattr( aduser, 'id' ) )
      ok_( hasattr( aduser, 'adaccounts' ) )
