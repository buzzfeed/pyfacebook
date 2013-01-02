from pyfacebook.models import Model

class AdStatistic( Model ):
  """
  The AdStatistic class represents an adstatistic objects in the Facebook Ads API:
  https://developers.facebook.com/docs/reference/ads-api/adstatistics

  """
  attrs_to_copy = ( 'id',
                    'account_id',
                    'adgroup_id',
                    'campaign_id',
                    'start_time',
                    'end_time',
                    'impressions',
                    'clicks',
                    'spent',
                    'social_impressions',
                    'social_clicks',
                    'social_spent',
                    'unique_impressions',
                    'unique_clicks',
                    'social_unique_impressions',
                    'social_unique_clicks'
                  )
