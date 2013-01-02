from pyfacebook.fault import Fault, FacebookException
from pyfacebook.models.adgroup import AdGroup

class AdGroupApi:

  def __init__(self, fb ):
    self.__fb = fb

  def __result_to_model(self, data):
    model = AdGroup()
    for key in data.keys():
      if hasattr( model, key ):
        setattr( model, key, data[key] )
    return model

  def find_by_adaccount_id( self, adaccount_id, include_deleted=False, limit=None, offset=None ):
    """
    Pulls ALL adgroups for a Facebook ads account

    :param int adaccount_id: The id corresponding to the Facebook account to pull adgroups from.
    :param boolean include_deleted: A flag that determines whether or not to include deleted adgroups in the resultset
    :param int limit: A limit for the number of adcampaign objects to request
    :param int limit: An offset for the adcampaign resultset

    :rtype ( [ AdGroup ], [ Fault ] ): A tuple of the AdGroups found, and any Faults encountered
    """
    try:
        if not adaccount_id:
            raise FacebookException( "Must pass an adaccount_id to this call" )

        if 'act_' not in adaccount_id:
            adaccount_id = 'act_' + adaccount_id

        params  = { }
        if include_deleted:
            params[ "include_deleted" ] = "true"
        if limit:
            params[ "limit" ] = str( limit )
        if offset:
            params[ "offset" ] = str( offset )
        
        return self.__fb.get_list_from_fb(adaccount_id, 'AdGroup', params)
    except:
        return [ ], [ Fault( ) ]

  def find_by_id( self, adgroup_id ):
    """
    Retrieves a single AdGroup object by adgroup ID

    :param int adgroup_id: The id for the adgroup

    :rtype AdGroup: The adgroup corresponding to the id
    """
    try:
      if not adgroup_id:
        raise FacebookException( "An adgroup_id is required." )
      return self.__fb.get_one_from_fb( adgroup_id, "AdGroup" ), [ ]
    except:
      return None, [ Fault( ) ]

  def find_by_ids( self, adgroup_ids ):
    """
    Retreives a list of AdGroup objects from a list of adgroup IDs subject to FB's max values for limit/batch size

    :param list adgroup_ids: The list of adgroup IDs we are searching for

    :rtype ( [ AdGroup ], [ Fault ] ): A tuple of AdGroup objects found, and any Faults encountered

    """
    return self.__fb.get_many_from_fb(adgroup_ids, 'AdGroup')
