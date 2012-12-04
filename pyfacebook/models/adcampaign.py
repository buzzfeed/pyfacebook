from pyfacebook.models import Model

class AdCampaign( Model ):

  attrs_to_copy = (
      'id',
      'account_id',
      'name',
      'start_time',
      'name',
      'end_time',
      'daily_budget',
      'campaign_status',
      'lifetime_budget' )