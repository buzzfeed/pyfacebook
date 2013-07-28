from pyfacebook.fault import FacebookException

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
    resp = {}
    inc_del = 'false'
    if include_deleted:
      inc_del = 'true'
    if not adaccount_id:
      raise FacebookException( "Must pass an adaccount_id to this call" )
    resp = self.__fb.get( '/act_' + str( adaccount_id ) + '/stats?include_deleted=' + str( inc_del ) )
    stat = self.__fb.adstatistic(resp)
    return stat, []

  def find_by_adgroup_ids( self, adgroup_ids, adaccount_id, include_deleted=False ):
    """
    Retrieves the Statistic object associated with this AdGroup

    :param boolean force_get: Set to true to force retrieval directly from Facebook. Otherwise this method will return objects from memory if available.

    :rtype: AdStatistic object associated with this AdGroup
    """
    if not adgroup_ids:
      raise FacebookException( "Must pass an adgroup_id list to this call" )

    if not adaccount_id:
      raise FacebookException( "Must pass an adaccount_id to this call" )

    if str( adaccount_id ).find( 'act_' ) < 0:
      adaccount_id = 'act_' + str( adaccount_id )

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

    return [self.__fb.adstatistic(stat) for stat in adstats]

  def find_by_start_time_end_time( self, adaccount_id, start_time, end_time, with_delivery=True, include_deleted=False ):
    """
    Retrieves a list of AdStatisics objects for a given AdAccount ID within a datetime range.
    AdStatistics returned will contain ONLY data that was generated within the specified datetime range.

    :param str adaccount_id: The adaccount ID that contains the desired adstatistics
    :param datetime start_time: The start of the datetime range. UTC only.
    :param datetime end_time: The end of the datetime range. UTC only.
    :param boolean with_delivery: If True, the call returns AdStatistics for ONLY AdGroups that generated data within the datetime range
    :param boolean include_deleted: Flag to determine whether we include AdStatistics for deleted AdGroup objects

    :rtype [AdStatistic]: A tuple which includes a list of AdStatistic objects found.

    """
    if not adaccount_id:
        raise FacebookException("Must pass an adaccount_id to this call")
    if (not start_time or not end_time):
        raise FacebookException("Must pass a start_time and end_time to this call")

    if 'act_' not in adaccount_id:
        adaccount_id = 'act_' + adaccount_id

    adstats = [ ]
    base_url       = '/' + adaccount_id + '/adgroupstats'
    start_time_str = start_time.strftime( "%Y-%m-%dT%H:%M:%S" )
    end_time_str   = end_time.strftime( "%Y-%m-%dT%H:%M:%S" )
    params = {"start_time": start_time_str,
              "end_time": end_time_str}

    if with_delivery:
        params["stats_mode"] = "with_delivery"
    if include_deleted:
        params["include_deleted"] = "true"

    adstats = self.__fb.get_all(base_url, params)
    return [self.__fb.adstatistic(adstat) for adstat in adstats]
