from pyfacebook.fault import Fault, FacebookException

class AdUserApi:

  def __init__(self, fb ):
    self.__fb = fb
    
  def find_by_adaccount_id( self, adaccount_id ):
    """
    Retrieves User objects associated with this AdAccount

    :param int adaccount_id: The adaccount id

    :rtype: List of AdUsers contained by this AdAccount

    """
    try:
      if not adaccount_id:
        raise FacebookException( "Must set an id before making this call" )
      resp  = self.__fb.get( '/act_' + str( adaccount_id ) + '/users' )
      users = resp['data']
      while True:
        if 'paging' in resp:
          if 'next' in resp['paging']:
            next = resp['paging']['next']
          else:
            break
        else:
          break
        resp   = self.__fb.get( next[26:] )
        users += resp['data']
      return [ self.__fb.aduser(aduser)[0] for aduser in users ], [ ]
    except:
      return [ ], [ Fault( ) ]