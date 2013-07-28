from pyfacebook.fault import FacebookException


class AdUserApi:

  def __init__(self, fb ):
    self.__fb = fb

  def find_by_adaccount_id( self, adaccount_id ):
    """
    Retrieves User objects associated with this AdAccount

    :param int adaccount_id: The adaccount id

    :rtype: List of AdUsers contained by this AdAccount

    """
    if not adaccount_id:
      raise FacebookException( "Must set an id before making this call" )
    users = self.__fb.get_all( '/act_' + str( adaccount_id ) + '/users' )
    return [ self.__fb.aduser(aduser) for aduser in users ]