from pyfacebook.models import Model

class AdAccount( Model ):
  """
  The AdAccount class represents the adaccount object in the Facebook Ads API:
  https://developers.facebook.com/docs/reference/ads-api/adaccount/

  """
  attrs_to_copy = ( 'id',
                    'account_id',
                    'name',
                    'account_status',
                    'currency',
                    'timezone_id',
                    'timezone_name',
                    'vat_status',
                    'daily_spend_limit',
                    'amount_spent',
                    'adusers',
                    'adgroups',
                    'adstatistic'
                  )