from pyfb import Pyfb
from urlparse import parse_qsl

from pyfacebook import utils
from pyfacebook.fault import Fault

from pyfacebook.models.adaccount import AdAccount
from pyfacebook.models.aduser import AdUser
from pyfacebook.models.adstatistic import AdStatistic
from pyfacebook.models.adgroup import AdGroup
from pyfacebook.models.adcampaign import AdCampaign
from pyfacebook.models.adcreative import AdCreative
from pyfacebook.models.adimage import AdImage

from pyfacebook.api.adaccount import AdAccountApi
from pyfacebook.api.aduser import AdUserApi
from pyfacebook.api.adstatistic import AdStatisticApi
from pyfacebook.api.adgroup import AdGroupApi
from pyfacebook.api.adcampaign import AdCampaignApi
from pyfacebook.api.adcreative import AdCreativeApi

import urllib
import json

class PyFacebook( object ):
  """
  The Facebook class's methods will return an object reflecting the Facebook Graph API

  """
  __app_id       = None
  __app_secret   = None
  __access_token = None
  __connection   = None

  def __init__( self, app_id, access_token=None, app_secret=None, raw_data=False ):
    """
    Initializes an object of the Facebook class. Sets local vars and establishes a connection.

    :param long app_id: Facebook app_id

    :param string app_secret: Facebook app_secret

    :param string access_token: Facebook access_token

    :param boolean raw_data: Reserved for future use

    """

    self.__app_id       = app_id
    self.__app_secret   = app_secret
    self.__access_token = access_token
    self.__connection   = Pyfb( app_id )
    self.__connection.set_access_token( access_token )

  def get_list_from_fb( self, container_obj_id, class_to_get ):
    """
    Retrieves data from Facebook and returns it as a list of objects.

    :param string container_obj_id: The id of the container object.

    :param string class_to_get: The class name of the object we are retrieving.

    :rtype: List of objects of Class class_to_get, representing data pulled from the Facebook Graph API

    """

    conn              = self.get_connection( )
    pyfb_objects      = conn._client.get_list( container_obj_id, utils.pluralize( class_to_get ) )
    new_local_objects = [ ]
    for pyfb_object in pyfb_objects:
      new_local_object, errors = self.get_instance( class_to_get, pyfb_object )
      self.copysome( pyfb_object, new_local_object, new_local_object.attrs_to_copy )
      new_local_objects.append( new_local_object )
    return new_local_objects

  def get_one_from_fb( self, reference_obj_id, class_to_get ):
    """
    Retrieves data from Facebook and returns it as an object.

    :param string reference_obj_id: The id of the reference object.

    :param string class_to_get: The class name of the object we are retrieving.

    :rtype: Object of Class class_to_get, representing data pulled from the Facebook Graph API

    """

    conn                     = self.get_connection( )
    pyfb_object              = conn._client.get_one( reference_obj_id, class_to_get )
    new_local_object, errors = self.get_instance( class_to_get, pyfb_object )
    return new_local_object

  def get_connection( self ):
    """
    Establishes a private __connection object, which is actually just an instance of Pyfb

    """

    if not self.__connection:
      self.__connection   = Pyfb( app_id )
      self.__connection.set_access_token( access_token )
    return self.__connection

  def get( self, resource, params={} ):
    url = "https://graph.facebook.com" + str( resource )
    if '?' in url:
      url += '&'
    else:
      url += '?'
    url += 'access_token=' + str( self.__access_token )
    if params:
      url += urllib.urlencode( params )
    raw_response = urllib.urlopen( url ).read( )
    return json.loads( raw_response )

  def get_access_token(self):
    return self.__access_token

  def custom_graph_call( self, url, return_class, qsl_call=False, requires_access_token=False ):
    """
    This method provides functionality to make special graph calls that are not supported by Pyfb

    :param string url: The FB Graph URL we are calling
    :param string return_class: The class name of the return object
    :param boolean qsl_call: Set to True if you expect the call to return a QSL object ( as opposed to JSON )

    :rtype: Response from the Facebook Graph API. For JSON calls (default) this is a list of dicts. For QSL calls this is a list of lists.
    """
    try:
      if requires_access_token:
        if '?' in url:
          url += '&'
        else:
          url += '?'
        url += 'access_token=' + str( self.__access_token )

      raw_response = urllib.urlopen( url ).read( )
      response     = None
      if qsl_call:
        response = parse_qsl( raw_response )
        if len( response ) == 0:
          ex = self.__connection._client.factory.make_object( 'Error', raw_response )
          raise FacebookException( str( "Facebook Graph API responded with Error: " + ex.error.message ) )
      else:
        response = self.__connection._client.factory.make_object( return_class, raw_response )
        if hasattr( response, 'error' ):
          ex = response
          raise FacebookException( str( "Facebook Graph API responded with Error: " + ex.error.message ) )
      return ( response, [ ] )
    except:
      return [ ], [ Fault( ) ]

  def exchange_token( self, facebook_token_url ):
    """
    Exchange an existing token for a new one. Token should be set ( and valid! ) before you call this.

    :rtype: New Facebook token
    """
    errors = [ ]

    try:
      facebook_token_url = "https://graph.facebook.com/oauth/access_token"
      if self.__app_id is None or self.__app_secret is None or self.__access_token is None:
        raise FacebookException( "Must set app_id, app_secret and access_token before calling exchange_token" )

      auth_exchange_params = self.__connection._client._get_url_path( {
        "client_id":         self.__app_id,
        "client_secret":     self.__app_secret,
        "grant_type":        "fb_exchange_token",
        "fb_exchange_token": self.__access_token
      } )
      auth_exchange_url     = "%s%s%s" % ( facebook_token_url, "?", auth_exchange_params )
      response, call_errors = self.custom_graph_call( auth_exchange_url, 'Token', qsl_call=True )
      errors                = errors + call_errors
      new_token             = response[ 0 ][ 1 ]
      self.__access_token   = new_token
      return ( new_token, [ ] )
    except:
      errors = errors + [ Fault( ) ]
      return [ ], errors

  def adaccount( self, pyfb_object )  :     return utils.wrapper( lambda: AdAccount( pyfb_object )   )
  def aduser( self, pyfb_object )     :     return utils.wrapper( lambda: AdUser( pyfb_object )      )
  def user( self, pyfb_object )       :     return utils.wrapper( lambda: AdUser( pyfb_object )      )
  def adstatistic( self, pyfb_object ):     return utils.wrapper( lambda: AdStatistic( pyfb_object ) )
  def stats( self, pyfb_object )      :     return utils.wrapper( lambda: AdStatistic( pyfb_object ) )
  def adgroup( self, pyfb_object )    :     return utils.wrapper( lambda: AdGroup( pyfb_object ) )
  def adcampaign( self, pyfb_object ) :     return utils.wrapper( lambda: AdCampaign( pyfb_object )  )
  def adcreative( self, pyfb_object ) :     return utils.wrapper( lambda: AdCreative( pyfb_object )  )
  def adimage( self, pyfb_object )    :     return utils.wrapper( lambda: AdImage( pyfb_object )     )

  def get_instance( self, classname, pyfb_object ):
    name = classname.lower( )
    if name == 'adaccount':
      return self.adaccount(pyfb_object)
    elif name == 'aduser':
      return self.aduser(pyfb_object)
    elif name == 'user':
      return self.user(pyfb_object)
    elif name == 'adstatistic':
      return self.adstatistic(pyfb_object)
    elif name == 'stats':
      return self.stats(pyfb_object)
    elif name == 'adgroup':
      return self.adgroup(pyfb_object)
    elif name == 'adcampaign':
      return self.adcampaign(pyfb_object)
    elif name == 'adcreative':
      return self.adcreative(pyfb_object)
    elif name == 'adimage':
      return self.adimage(pyfb_object)
    else:
      raise FacebookException( "Unrecognized object requested." )

  def api(self):
    return FacebookApi( self )

class FacebookApi( PyFacebook ):
  def __init__(self, fb): self.__fb = fb
  def adaccount(self):   return AdAccountApi(self.__fb)
  def adcampaign(self):  return AdCampaignApi(self.__fb)
  def adcreative(self):  return AdCreativeApi(self.__fb)
  def adgroup(self):     return AdGroupApi(self.__fb)
  def adstatistic(self): return AdStatisticApi(self.__fb)
  def aduser(self):      return AdUserApi(self.__fb)
