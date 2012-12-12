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

  def create(self, account_id, name=None, acreative_type='25', object_id=None, body=None, image_hash=None, image_url=None, creative_id=None, count_current_adgroups=None, title=None, run_status=None, link_url=None, url_tags=None, preview_url=None, related_fan_page=None, follow_redirect=None, auto_update=None, story_id=None, action_spec=None):
    """
    Creates a new AdCreative using the given parameters. For more information visit: https://developers.facebook.com/docs/reference/ads-api/creative-specs/

    :param string name The name of the creative in the creative library
    :param string acreative_type The number of the ad type, which identifies the type of Sponsored story or ad
    :param int object_id The Facebook object ID that is relevant to the ad and ad type. See connection objects)
    :param string body The body of the ad, not applicable to Sponsored stories
    :param string image_hash Image ID for an image you can use in creatives and thus in ads.
    :param string image_url A URL for the image for this creative.
    :param int creative_id Required in order to use an existing creative from the creative library.
    :param string count_current_adgroups Indicates the number of ad groups in which the creative is used.
    :param string title Title for a default ad.
    :param int run_status Indicates whether the creative is active (1) or deleted (3).
    :param string link_url A URL for the ad.
    :param string url_tags A string which will be appended to urls clicked from type 25, 27, and 31 creatives. Note Optional URL Tags are not supported for Open Graph Sponsored Stories in the news feed.
    :param string preview_url The URL to preview the ad, only for the current session user.
    :param string related_fan_page Provides social context to a type 1 ad, see Including social context. Defaults to '1' if not specified.
    :param boolean follow_redirect When adding social context to a type 1 ad, indicates that Facebook should follow any HTTP redirects encountered at the link_url in order to find the Facebook object to apply social context from.
    :param boolean auto_update Boolean true to constantly promote the latest page post and ignore story_id parameter. Boolean false to promote a specific page post by story_id. Required for type 27 ads only.
    :param string story_id The fbid of a page post to use in a type 25 or type 27 ad. This ID can be retrieved by using the graph API to query the posts of the page. Note: The ID of the post is returned in the following format: <Page_ID>_<Story_ID>. Only the "Story_ID" element should be supplied as the story_id.
    :param string(JSON) action_spec A JSON string defining an action performed by a user for use in a type 25 ad. See action spec reference for more details.

    :rtype tuple the new adcreative and any raised errors.
    """

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
