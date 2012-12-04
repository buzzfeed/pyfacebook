from pyfacebook.models import Model

class AdUser( Model ):
  """
  The AdUser class represents the aduser object in the Facebook Ads API:
  https://developers.facebook.com/docs/reference/ads-api/aduser/
  We extend the functionality in the documentation with custom calls for adaccounts

  """

  attrs_to_copy = ( 'id', 'adaccounts', 'role' )