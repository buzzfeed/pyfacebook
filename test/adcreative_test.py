import json
import time

from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID
from pyfacebook import PyFacebook

from nose.tools import eq_, ok_

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
      'adcreative_type': 25,
      'action_spec': json.dumps({'action.type': 'app_use', 'application': FACEBOOK_APP_ID})
    }
    created_obj, errors = self.fb.api().adcreative().create(FACEBOOK_TEST_ACCOUNT_ID, **params)
    ok_(not not created_obj.id)
    fetched_obj = self.fb.get_one_from_fb(created_obj.id, 'AdCreative')
    eq_(fetched_obj.id, created_obj.id)
    eq_(fetched_obj.type, params['adcreative_type'])

    param_spec = json.loads(params['action_spec'])
    action_spec = fetched_obj.action_spec
    eq_(str(action_spec['application']), param_spec['application'])
    eq_(str(action_spec['action.type']), param_spec['action.type'])

  def test_update(self):
    params = {
      'adcreative_type': 25,
      'action_spec': json.dumps({'action.type': 'app_use', 'application': FACEBOOK_APP_ID})
    }
    adcreative, errors = self.fb.api().adcreative().create(FACEBOOK_TEST_ACCOUNT_ID, **params)
    params = {'name': 'test' + str( time.time() * 10000 ) }
    success, errors = self.fb.api().adcreative().update(adcreative.id, **params)
    if errors:
        for error in errors:
            print error.message
            for t in error.tb:
                print t
    ok_(success)
    updated_obj = self.fb.get_one_from_fb(adcreative.id, 'AdCreative')
    eq_(updated_obj.id, adcreative.id)
    eq_(updated_obj.name, params['name'])
