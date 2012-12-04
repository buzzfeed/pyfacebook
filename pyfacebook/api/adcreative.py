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