from pyfacebook.fault import Fault, FacebookException

class AdAccountApi:
  
  def __init__(self, fb ):
    self.__fb = fb

  def find_by_id( self, adaccount_id ):
    """
    Retrieves an AdAccount by the id.

    :param int adaccount_id: The id for the adaccount

    :rtype AdAccount: The AdAccount associated with the id
    """
    try:
      if not adaccount_id:
        raise FacebookException( "Must pass an adaccount_id" )
      return self.__fb.get_one_from_fb( adaccount_id, "AdAccount" ), []
    except:
      return [], [Fault()]