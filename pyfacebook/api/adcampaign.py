from pyfacebook.fault import Fault, FacebookException

class AdCampaignApi:

  def __init__(self, fb ):
    self.__fb = fb
    
  def find_by_adgroup_id( self, adgroup_id ):
    """
    Retriees the AdCampaign object associated with this AdGroup

    :param int adgroup_id: The id for the adgroup

    :rtype: AdCampaign the AdCampaign object associated with this AdGroup
    """

    try:
      if not adgroup_id:
        raise FacebookException( "Must set an id before making this call" )
      adgroup, errs = self.__fb.api().adgroup().find_by_id( adgroup_id )
      if errs:
        return None, errs
      campaign_id = adgroup.campaign_id
      return self.__fb.get_one_from_fb( campaign_id, "AdCampaign" ), []
    except:
      return [], [Fault()]

  def find_by_id( self, adcampaign_id ):
    """
    Retrieves the AdCampaign object corresponding to the object id passed

    :param int adcampaign_id: The id for the adcampaign from the perspective of Facebook

    :rtype AdCampaign:
    """
    try:
      return self.__fb.get_one_from_fb( adcampaign_id, "AdCampaign" ), []
    except:
      return None, [Fault()]