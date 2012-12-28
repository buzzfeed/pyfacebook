import datetime
import pytz

from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID
from pyfacebook.settings import FACEBOOK_PROD_ACCOUNT_ID

from pyfacebook import PyFacebook

from nose.tools import eq_, ok_

class TestAdStatisticApi( ):

  def setUp(self):
    self.fb = PyFacebook( app_id=FACEBOOK_APP_ID,
                          access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                          app_secret=FACEBOOK_APP_SECRET )

  def test_find_by_id(self):
    adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID )
    adgroup          = adgroups[0]

    adgroup_by_id, errors = self.fb.api().adgroup().find_by_id( adgroup.id )

    eq_( adgroup.__dict__, adgroup_by_id.__dict__ )

  def one_percent_more(self, somevalue):
    return somevalue + 0.01 * somevalue

  def one_percent_less(self, somevalue):
    return somevalue - 0.01 * somevalue

  def test_find_by_adaccount_id_and_find_by_adgroup_ids(self):
    include_deleted = True
    adgroups, errors = self.fb.api().adgroup().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID, include_deleted=include_deleted )
    ok_( not errors )
    adstat_by_account_id, errors = self.fb.api().adstatistic().find_by_adaccount_id( FACEBOOK_TEST_ACCOUNT_ID, include_deleted=include_deleted )
    ok_( not errors )

    all_stats = {
      'social_unique_clicks'      : 0,
      'unique_impressions'        : 0,
      'social_clicks'             : 0,
      'social_impressions'        : 0,
      'social_unique_impressions' : 0,
      'social_spent'              : 0,
      'impressions'               : 0,
      'clicks'                    : 0,
      'unique_clicks'             : 0
    }

    stats, errors = self.fb.api().adstatistic().find_by_adgroup_ids( [ adgroup.id for adgroup in adgroups ], FACEBOOK_PROD_ACCOUNT_ID, include_deleted=include_deleted )

    for stat in stats:
      for key, val in all_stats.items():
        addtl_val = None
        if hasattr( stat, key ):
          addtl_val = getattr( stat, key )
        if addtl_val:
          all_stats[ key ] = val + addtl_val

    totals = {
      'social_spent': 84,
      'social_clicks': 2,
      'social_unique_clicks': 0,
      'social_impressions': 309,
      'social_unique_impressions': 0,
      'unique_impressions': 0,
      'impressions': 20854182,
      'clicks': 35022,
      'unique_clicks': 0
    }

    for key, val in all_stats.items():
      to_compare = totals[key]

      ok_( val > self.one_percent_less( to_compare ) or val == int( to_compare ) )
      ok_( val < self.one_percent_more( to_compare ) or val == int( to_compare ) )

  def test_find_by_start_time_end_time( self ):
    utc             = pytz.utc
    include_deleted = True

    expected_stats = {
      'adgroup_id'                : 6006750140365,
      'campaign_id'               : 6006664880365,
      'start_time'                : '2012-12-26T06:00:00+0000',
      'end_time'                  : '2012-12-27T06:00:00+0000',
      'impressions'               : 44390,
      'clicks'                    : 9,
      'spent'                     : 414,
      'unique_impressions'        : 0,
      'unique_clicks'             : 0,
      'social_impressions'        : 0,
      'social_clicks'             : 0,
      'social_spent'              : 0,
      'social_unique_impressions' : 0,
      'social_unique_clicks'      : 0
    }

    # Test single day
    start_time = datetime.datetime( 2012, 12, 26, 6, 0, 0, tzinfo=utc )
    end_time   = datetime.datetime( 2012, 12, 27, 6, 0, 0, tzinfo=utc )
    stats, errors = self.fb.api().adstatistic().find_by_start_time_end_time( FACEBOOK_PROD_ACCOUNT_ID, start_time, end_time )

    eq_( len( errors ), 0 )
    eq_( len( stats ), 60 )

    stat_to_compare = stats[ 0 ]

    for key, val in expected_stats.items():

      eq_( expected_stats[ key ], getattr( stat_to_compare, key ) )

    # Test one month: paging
    start_time = datetime.datetime( 2012, 11, 26, 6, 0, 0, tzinfo=utc )
    end_time   = datetime.datetime( 2012, 12, 27, 6, 0, 0, tzinfo=utc )
    stats, errors = self.fb.api().adstatistic().find_by_start_time_end_time( FACEBOOK_PROD_ACCOUNT_ID, start_time, end_time )

    eq_( len( errors ), 0 )
    eq_( len( stats ), 428 )

