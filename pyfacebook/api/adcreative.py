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

  def create(self, account_id, acreative_type=25, **kwargs):
    kwargs.update(account_id=account_id, type=acreative_type)
    kwargs = self.__fb.clean_params(**kwargs)
    adcreative, model, errors = self.__fb.create('AdCreative', **kwargs)
    if errors:
      errors.append(Fault(message='AdCreative Type is %s' % acreative_type))
      return None, errors

    return model, []

  def update(self, adcreative_id, **kwargs):
    kwargs = self.__fb.clean_params(**kwargs)
    result, errors = self.__fb.update(adcreative_id, **kwargs)
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
