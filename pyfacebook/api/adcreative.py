from pyfacebook.fault import Fault, FacebookException

class AdCreativeApi:

  def __init__(self, fb ):
    self.__fb = fb

  def find_by_adgroup_id( self, adgroup_id ):
    """
    Retrieves the adcreatives for an adgroup object. Facebook ambiguously defines whether there are many or just one associated.

    :param int adgroup_id: The adgroup id to search by

    :rtype: AdCreative object associated with the AdGroup
    """
    try:
      if not adgroup_id:
        raise FacebookException( "Must set an id before making this call" )
      adgroup = self.__fb.get_one_from_fb( adgroup_id, "AdCreative" )
      adcreatives = [ ]
      for creative_id in adgroup.creative_ids:
        adcreatives.append( self.__fb.get_one_from_fb( creative_id, "AdCreative" ) ) # TODO: This should be a batch request
      return adcreatives, []
    except:
      return None, [Fault()]

  def create(self, account_id, adgroup_id, name, body, link_url, max_bid, bid_type, ad_status, creative_ids, start_time, end_time, title, targeting):
    kwargs = {
      'account_id': account_id,
      'adgroup_id': adgroup_id,
      'name': name,
      'body': body,
      'link_url': link_url,
      'max_bid': max_bid,
      'bid_type': bid_type,
      'ad_status': ad_status,
      'creative_ids': creative_ids,
      'start_time': start_time,
      'end_time': end_time,
      'title': title,
      'targeting': targeting
    }
    adcreative, model, errors = self.__fb.create('AdCreative', **kwargs)
    if errors:
      return None, errors
    setattr(model, 'ad_id', adcreative['id'])
    return model, []

  def update(self, adcreative_id, adgroup_id=None, name=None, body=None, link_url=None, max_bid=0, bid_type=0, ad_status=None, creative_ids=None, start_time=None, end_time=None, title=None, targeting=None):
    kwargs = {
      'adgroup_id': adgroup_id,
      'name': name,
      'body': body,
      'link_url': link_url,
      'max_bid': max_bid,
      'bid_type': bid_type,
      'ad_status': ad_status,
      'creative_ids': creative_ids,
      'start_time': start_time,
      'end_time': end_time,
      'title': title,
      'targeting': targeting
    }
    kwargs = self.__fb._clean_params(kwargs)
    result, errors = self.update(adcreative_id, **kwargs)
    if errors:
      return None, errors
    if result != True:
      return None, [Fault(message='Request could not be completed. Result was <%s>' % res)]

    return result, []

  def __result_to_model(self, data):
    ag = self.adgroup()
    for key in data.keys():
      if hasattr( ag ):
        setattr( ag, key, data[key] )
    return ag
