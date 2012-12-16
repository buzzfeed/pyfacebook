from pyfacebook.models import Model

class AdGroup( Model ):
  """
  The AdGroup class represents an adgroup object in the Facebook Ads API:
  https://developers.facebook.com/docs/reference/ads-api/adgroup

  """
  attrs_to_copy    = ( 'id',
                       'campaign_id',
                       'adgroup_id',
                       'name',
                       'disapprove_reason_descriptions',
                       'adgroup_status',
                       'ad_status',
                       'bid_info',
                       'bid_type',
                       'max_bid',
                       'start_time',
                       'end_time',
                       'updated_time',
                       'adaccount',
                       'adcampaign',
                       'targeting',
                       'creative_ids',
                       'ad_id',
                       'adstatistic',
                     )