from pyfacebook.fault import FacebookException


class AdCampaignApi:

  def __init__(self, fb):
    self.__fb = fb

  def find_by_adaccount_id( self, adaccount_id, include_deleted=False, limit=None, offset=None ):
    """
    Pulls ALL adcampaigns for a Facebook ads account

    :param int adaccount_id: The id corresponding to the Facebook account to pull adcampaigns from.
    :param boolean include_deleted: A flag that determines whether or not to include deleted adcampaigns in the resultset
    :param int limit: A limit for the number of adcampaign objects to request
    :param int offset: An offset for the adcampaign resultset

    :rtype [ AdCampaign ]: A list of the AdCampaigns found.
    """
    if not adaccount_id or type(adaccount_id) not in (str, unicode):
        raise FacebookException("Must pass an adaccount_id of type in ( str, unicode ) to this call")

    if 'act_' not in adaccount_id:
        adaccount_id = 'act_' + adaccount_id

    params = {}
    if include_deleted:
        params["include_deleted"] = "true"
    if limit:
        params["limit"] = str(limit)
    if offset:
        params["offset"] = str(offset)

    return self.__fb.get_list_from_fb(adaccount_id, 'AdCampaign', params)

  def find_by_adgroup_id( self, adgroup_id ):
    """
    Retriees the AdCampaign object associated with this AdGroup

    :param int adgroup_id: The id for the adgroup

    :rtype: AdCampaign the AdCampaign object associated with this AdGroup
    """
    if not adgroup_id:
      raise FacebookException("Must set an id before making this call")
    adgroup = self.__fb.api().adgroup().find_by_id(adgroup_id)
    campaign_id = adgroup.campaign_id
    return self.__fb.get_one_from_fb(campaign_id, "AdCampaign")

  def find_by_id( self, adcampaign_id ):
    """
    Retrieves the AdCampaign object corresponding to the object id passed

    :param int adcampaign_id: The id for the adcampaign from the perspective of Facebook

    :rtype AdCampaign:
    """
    return self.__fb.get_one_from_fb(adcampaign_id, "AdCampaign")

  def find_by_ids( self, adcampaign_ids ):
    """
    Retreives a list of AdCampaign objects from a list of adcampaign IDs subject to Facebook's max limit/batch size

    :param list adcampaign_ids: The list of adcampaign IDs we are searching for

    :rtype [AdCampaign]: A list of AdCampaign objects found.

    """
    return self.__fb.get_many_from_fb(adcampaign_ids, 'AdCampaign')
