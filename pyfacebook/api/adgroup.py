from pyfacebook.fault import Fault, FacebookException

class AdGroupApi:

  def __init__(self, fb ):
    self.__fb = fb

  def find_by_adaccount_id( self, account_id, include_deleted=False ):
    """
    Pulls ALL adgroups from Facebook that don't have SocialAd counterparts locally. This method has no regard for active/inactive adgroups.

    :param Facebook fb: An instance of the Facebook api class.
    :param int account_id: The id corresponding to the Facebook account to pull adgroups from.

    :rtype list(AdGroup): All the new adgroups!
    """
    try:
      next           = False
      ad_group_dicts = [ ]
      ad_groups      = [ ]
      while True:
        if next:
          resp = self.__fb.get( next )
        else:
          url  = '/act_' + str( account_id ) + '/adgroups?access_token=' + str( self.__fb.access_token() )
          if include_deleted:
            url += '&include_deleted=true'
          resp = self.__fb.get( url )
        if 'data' not in resp:
          raise Exception( "'data' not in response: " + str( resp ) )
        ad_group_dicts = ad_group_dicts + resp[ 'data' ]
        if 'paging' in resp:
          if 'next' in resp['paging']:
            next = resp['paging'][ 'next' ][26:]
          else:
            break
        else:
          break
      for entry in ad_group_dicts:        
        ad_group, errors   = self.__fb.adgroup( entry )
        ad_groups.append( ad_group )
    except:
      return None, [Fault()]
    return ad_groups, []

  def find_by_id( self, adgroup_id ):
    """
    Retrieves AdGroup objects by vendor id

    :param int adgroup_id: The id for the adgroup

    :rtype AdGroup: The adgroup corresponding to the id
    """
    try:
      if not adgroup_id:
        raise FacebookException( "An adgroup_id is required." )
      return self.__fb.get_one_from_fb( adgroup_id, "AdGroup" ), [ ]
    except:
      return None, [ Fault( ) ]
