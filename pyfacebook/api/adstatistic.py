from pyfacebook.fault import Fault, FacebookException

from discotech.settings import FACEBOOK_PROD_ACCOUNT_ID

class AdStatisticApi:

  def __init__( self, fb ):
    self.__fb = fb

  def find_by_adaccount_id( self, adaccount_id, include_deleted=False ):
    """
    Retrieves Statistic objects associated with this AdAccount

    :param int adaccount_id: The adaccount id
    :param bool include_deleted: Includes deleted adstatistics if set to True

    :rtype: AdStatistic object associated with this AdAccount
    """
    try:
      resp       = {}
      inc_del = 'false'
      if include_deleted:
        inc_del = 'true'
      if not adaccount_id:
        raise FacebookException( "Must pass an adaccount_id to this call" )
      resp = self.__fb.get( '/act_' + str( adaccount_id ) + '/stats?include_deleted=' + str( inc_del ) )
      stat, errors = self.__fb.adstatistic(resp)
    except:
      return None, [ Fault( ) ]
    return stat, [ ]

  def find_by_adgroup_ids( self, adgroup_ids, include_deleted=False ):
    """
    Retrieves the Statistic object associated with this AdGroup

    :param boolean force_get: Set to true to force retrieval directly from Facebook. Otherwise this method will return objects from memory if available.

    :rtype: AdStatistic object associated with this AdGroup
    """
    try:
      if not adgroup_ids:
        raise FacebookException( "Must pass an adgroup_id list to this call" )

      adaccount_id = 'act_' + str( FACEBOOK_PROD_ACCOUNT_ID )

      num_ids   = len( adgroup_ids )
      batch     = 0
      batchsize = 50
      adstats   = [ ]

      while True:
        adgroup_id_batch = adgroup_ids[batch*batchsize:batch*batchsize+batchsize]
        url              = '/' + adaccount_id + '/adgroupstats?adgroup_ids=' + '[' + ",".join(adgroup_id_batch) + ']'
        if include_deleted:
          url += '&include_deleted=true'
        resp             = self.__fb.get( url )
        batch            = batch + 1
        adstats          = adstats + resp['data']

        if batch * batchsize + batchsize > num_ids:
          if num_ids is not batch*batchsize:
            url     = '/' + adaccount_id + '/adgroupstats?adgroup_ids=' + '[' + ",".join(adgroup_ids[batch*batchsize:num_ids]) + ']'
            if include_deleted:
              url += '&include_deleted=true'
            resp    = self.__fb.get( url )
            adstats = adstats + resp['data']
          break

      return [ self.__fb.adstatistic( stat )[0] for stat in adstats ] , []
    except:
      return [ ], [ Fault( ) ]