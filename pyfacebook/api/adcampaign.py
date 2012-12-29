from pyfacebook.fault import Fault, FacebookException

class AdCampaignApi:

  def __init__(self, fb ):
    self.__fb = fb

  def find_by_adaccount_id( self, adaccount_id, include_deleted=False, limit=None, offset=None ):
    """
    Pulls ALL adcampaigns for a Facebook ads account

    :param int adaccount_id: The id corresponding to the Facebook account to pull adcampaigns from.
    :param boolean include_deleted: A flag that determines whether or not to include deleted adcampaigns in the resultset
    :param int limit: A limit for the number of adcampaign objects to request
    :param int limit: An offset for the adcampaign resultset

    :rtype ( [ AdCampaign ], [ Fault ] ): A tuple of the AdCampaigns found, and any Faults encountered
    """
    try:
        if not adaccount_id:
            raise FacebookException( "Must pass an adaccount_id to this call" )

        if 'act_' not in adaccount_id:
            adaccount_id = 'act_' + adaccount_id

        adcampaigns = [ ]
        resp        = [ ]
        base_url       = '/' + adaccount_id + '/adcampaigns'
        params  = { }

        if include_deleted:
            params[ "include_deleted" ] = "true"
        if limit:
            params[ "limit" ] = str( limit )
        if offset:
            params[ "offset" ] = str( offset )

        if not limit:
          resp     = self.__fb.get( base_url, params, with_paging=True )
        else:
          resp     = self.__fb.get( base_url, params, with_paging=False )

        adcampaigns += resp[ 'data' ]

        return [ self.__fb.adcampaign( adcampaign )[ 0 ] for adcampaign in adcampaigns ] , [ ]
    except:
      return [ ], [ Fault( ) ]

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

  def find_by_ids( self, adcampaign_ids ):
    """
    Retreives a list of AdCampaign objects from a list of adcampaign IDs

    :param list adcampaign_ids: The list of adcampaign IDs we are searching for

    :rtype ( [ AdCampaign ], [ Fault ] ): A tuple of AdCampaign objects found, and any Faults encountered

    """
    try:
      if not adcampaign_ids or len( adcampaign_ids ) == 0:
        raise FacebookException( "A list of adcampaign_ids is required" )
      adcampaigns = [ ]
      base_url = ''
      params   = { }
      params[ "ids" ] = ",".join( map( str, adcampaign_ids ) )

      resp      = self.__fb.get( base_url, params )
      adcampaigns += resp

      return [ self.__fb.adcampaign( adcampaign )[ 0 ] for adcampaign in adcampaigns ], [ ]
    except:
      return [ ], [ Fault( ) ]
