import sys
import urllib
import urllib2
import json
from urlparse import parse_qsl

from pyfacebook import utils
from pyfacebook.fault import Fault, FacebookException

from pyfacebook import models
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


class PyFacebook( object ):
  """
  The Facebook class's methods will return an object reflecting the Facebook Graph API

  """
  __app_id         = None
  __app_secret     = None
  __access_token   = None
  __graph_endpoint = "https://graph.facebook.com"

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

  def get_list_from_fb( self, container_obj_id, class_to_get ):
    """
    Retrieves data from Facebook and returns it as a list of objects.

    :param string container_obj_id: The id of the container object.

    :param string class_to_get: The class name of the object we are retrieving.

    :rtype: List of objects of Class class_to_get, representing data pulled from the Facebook Graph API

    """
    resp = self.get( '/' + str( container_obj_id ) + '/' + class_to_get.lower() )
    return [ self.get_instance( class_to_get, obj )[0] for obj in resp ]

  def get_one_from_fb( self, reference_obj_id, class_to_get ):
    """
    Retrieves data from Facebook and returns it as an object.

    :param string reference_obj_id: The id of the reference object.

    :param string class_to_get: The class name of the object we are retrieving.

    :rtype: Object of Class class_to_get, representing data pulled from the Facebook Graph API

    """
    resp = self.get( '/' + str( reference_obj_id ) )
    return self.get_instance( class_to_get, resp )[0]

  def create(self, model, **kwargs):
    """
    Creates a new instance on type <model> with the given <kwargs>

    :param string model The handle of the model we're creating

    :rtype tuple A dict with the attributes of the remote obj, the new model instance with the given attributes and the errors raised, if any.
    """
    try:
      account_id = kwargs.pop('account_id')
    except KeyError:
      raise FacebookException('An account_id is required to make the request!')

    try:
      url = '/act_{account_id}/{model}s'.format(account_id=account_id, model=model.lower())
      response = self.post(url, urllib.urlencode(kwargs))
      instance, errors = self.get_instance(model, kwargs)
      if 'id' in response:
        setattr(instance, 'id', response['id'])
    except:
      return None, [Fault()]
    return instance, []

  def update(self, obj_id, **kwargs):
    """
    Sends an update request for obj_id with the given kwargs.

    :rtype dict The data retrieved by the request after updating.
    """
    try:
      url = '/{obj_id}'.format(obj_id=obj_id)
      response = self.post(url, urllib.urlencode(kwargs))
    except:
      return None, [Fault()]
    return response, []

  def clean_params(self, clean_empty_strings=True, **kwargs):
    """
    Remove null and falsy values from an argument list.
    """
    cleaned_data = dict()
    for k, v in kwargs.iteritems():
      if not v:
        if isinstance(v, str) and not clean_empty_strings:
          cleaned_data[k] = v
      else:
        cleaned_data[k] = v
    return kwargs

  def get( self, resource, params={} ):
    url = self.__graph_endpoint + str( resource )
    if '?' in url:
      url += '&'
    else:
      url += '?'
    url += 'access_token=' + str( self.__access_token )
    if params:
      url += '&'
      url += urllib.urlencode( params )
    response = urllib.urlopen(url)
    raw_response = response.read( )
    obj = json.loads( raw_response )
    if 'error' in obj:
      raise FacebookException( obj['error'] )
    response.close()
    return obj

  def post(self, resource, payload ):
    """
    Issues an HTTP POST request to the resource with params as the payload
    """
    url = '{base_url}{source_url}'.format(base_url=self.__graph_endpoint, source_url=str(resource))
    url += '&' if '?' in url else '?'
    url += urllib.urlencode({'access_token': self.access_token()})
    response = urllib.urlopen(url, payload)
    raw_response = response.read()
    obj = json.loads( raw_response )
    try:
      if 'error' in obj:
        raise FacebookException( obj['error'] )
    except TypeError:  # update calls simply return True, so it's not iterable, but correct
      pass
    response.close()
    return obj

  def delete(self, resource, params, content_type='application/json'):
    """
    Issues an HTTP DELETE request to the resource with params as the payload
    """
    url = self.__graph_endpoint + str(resource)
    opener = urllib2.build_opener(urllib2.HTTPSHandler)
    request = urllib2.Request(url, data=params)
    request.add_header('Content-Type', content_type)
    request.get_method = lambda: 'DELETE'
    response = opener.open(request)
    raw_response = response.read()
    response.close()
    return raw_response

  def access_token(self, access_token=None):
    if access_token:
      self.__access_token = access_token
    return self.__access_token

  def exchange_token( self ):
    """
    Exchange an existing token for a new one. Token should be set ( and valid! ) before you call this.

    :rtype: New Facebook token
    """
    errors = [ ]

    try:
      facebook_token_url = self.__graph_endpoint + '/oauth/access_token'
      if self.__app_id is None or self.__app_secret is None or self.__access_token is None:
        raise FacebookException( "Must set app_id, app_secret and access_token before calling exchange_token" )

      auth_exchange_params = {
        "client_id":         self.__app_id,
        "client_secret":     self.__app_secret,
        "grant_type":        "fb_exchange_token",
        "fb_exchange_token": self.__access_token
      }
      auth_exchange_url     = "%s%s%s" % ( facebook_token_url, "?", auth_exchange_params )
      response, call_errors = self.get( auth_exchange_url )
      new_token             = response[ 0 ][ 1 ]
      self.__access_token   = new_token
      return ( new_token, [ ] )
    except:
      errors = errors + [ Fault( ) ]
      return [ ], errors

  def adaccount( self, o )  :     return utils.wrapper( lambda: AdAccount( o )   )
  def aduser( self, o )     :     return utils.wrapper( lambda: AdUser( o )      )
  def user( self, o )       :     return utils.wrapper( lambda: AdUser( o )      )
  def adstatistic( self, o ):     return utils.wrapper( lambda: AdStatistic( o ) )
  def stats( self, o )      :     return utils.wrapper( lambda: AdStatistic( o ) )
  def adgroup( self, o )    :     return utils.wrapper( lambda: AdGroup( o ) )
  def adcampaign( self, o ) :     return utils.wrapper( lambda: AdCampaign( o )  )
  def adcreative( self, o ) :     return utils.wrapper( lambda: AdCreative( o )  )
  def adimage( self, o )    :     return utils.wrapper( lambda: AdImage( o )     )

  def get_instance(self, classname, o):
    """
    Returns an initialized instance of the class given by classname.

    :param string classname The name of the module containing the needed class.

    :param dict o A dictionary containing arguments to initialize a instance of the requested class.
    """
    try:
      return getattr(self, classname.lower())(o)
    except AttributeError:
      raise FacebookException("Unrecognized object requested.")

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
