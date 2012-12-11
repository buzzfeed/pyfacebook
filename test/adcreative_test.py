import json
from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID
from pyfacebook import PyFacebook
from nose.tools import ok_

class TestAdCreativeApi( ):
  def setUp(self):
    self.fb = PyFacebook( app_id=FACEBOOK_APP_ID,
                          access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                          app_secret=FACEBOOK_APP_SECRET )

  def test_find_by_adgroup_id(self):
    adgroups, errors    = self.fb.api().adgroup().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID )
    adgroup             = adgroups[ 0 ]
    adcreatives, errors = self.fb.api().adcreative().find_by_adgroup_id( adgroup.id )
    adcreative          = adcreatives[ 0 ]

    ok_( not not adcreative.body ) # Just checking the attributes are there.
    ok_( not not adcreative.name )
    ok_( not not adcreative.link_url )
    ok_( not not adcreative.title )

  def test_create(self):
    params = {
      'acreative_type': 25,
      'action_spec': json.dumps({'action.type': 'app_use', 'application': FACEBOOK_APP_ID})
    }
    adcreative, errors = self.fb.api().adcreative().create(FACEBOOK_TEST_ACCOUNT_ID, **params)
    ok_(not not adcreative.id)

  def test_update(self):
    params = {
      'acreative_type': 25,
      'action_spec': json.dumps({'action.type': 'app_use', 'application': FACEBOOK_APP_ID})
    }
    adcreative, errors = self.fb.api().adcreative().create(FACEBOOK_TEST_ACCOUNT_ID, **params)
    params = {'name': 'test'}
    success, errors = self.fb.api().adcreative().update(adcreative.id, **params)
    ok_(success)
    updated_obj = self.fb.get_one_from_fb(adcreative.id, 'AdCreative')
    ok_(updated_obj.id == adcreative.id)
    ok_(updated_obj.name == params['name'])
