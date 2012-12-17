from pyfacebook.models import Model


class AdCreative( Model ):
  """
  The AdCreative class represents the adcreative object in the Facebook Ads API:
  https://developers.facebook.com/docs/reference/ads-api/adcreative

  """
  attrs_to_copy = (
    'id',
    'adgroup_id',
    'created_time',
    'name',
    'body',
    'link_url',
    'max_bid',
    'bid_type',
    'ad_id',
    'ad_status',
    'creative_ids',
    'start_time',
    'end_time',
    'title',
    'account_id',
    'updated_time',
    'targeting',
    'impression_control_map',
    'spec',
    'action_spec',
    'type'
  )
