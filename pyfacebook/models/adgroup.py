from pyfacebook.models import Model

class AdGroup( Model ):
  """
  The AdGroup class represents an adgroup object in the Facebook Ads API:
  https://developers.facebook.com/docs/reference/ads-api/adgroup

  """
  attrs_to_copy    = ( 'id',
                       'campaign_id',
                       'ad_id',
                       'name',
                       'disapprove_reason_descriptions',
                       'adgroup_status',
                       'bid_type',
                       'max_bid',
                       'start_time',
                       'end_time',
                       'updated_time',
                       'adaccount',
                       'adcampaign',
                       'targetingspecs',
                       'adcreative',
                       'adstatistic'
                     )