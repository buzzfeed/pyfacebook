from pyfacebook.fault import FacebookException


class AdCreativeApi:

    def __init__(self, fb):
        self.__fb = fb

    def find_by_adaccount_id(self, adaccount_id, include_deleted=False, limit=None, offset=None):
        """
        Pulls ALL adcreatives for a Facebook ads account

        :param int adaccount_id: The id corresponding to the Facebook account to pull adcreatives from.
        :param boolean include_deleted: A flag that determines whether or not to include deleted adcreatives in the resultset
        :param int limit: A limit for the number of adcampaign objects to request
        :param int offset: An offset for the adcampaign resultset

        :rtype [ AdCreative ]: A list of the AdCreatives found.
        """
        if not adaccount_id or type(adaccount_id) not in (str, unicode):
            raise FacebookException("Must pass an adaccount_id to this call")

        if 'act_' not in adaccount_id:
            adaccount_id = 'act_' + adaccount_id

        params = {}
        if include_deleted:
            params["include_deleted"] = "true"
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)

        return self.__fb.get_list_from_fb(adaccount_id, 'AdCreative', params)

    def find_by_adgroup_id(self, adgroup_id):
        """
        Retrieves the adcreatives for an adgroup object. Facebook ambiguously defines whether there are many or just one associated.

        :param int adgroup_id: The adgroup id to search by

        :rtype: AdCreative object associated with the AdGroup
        """
        if not adgroup_id:
            raise FacebookException("Must set an id before making this call")
        adgroup = self.__fb.get_one_from_fb(adgroup_id, "AdCreative")
        adcreatives = []
        for creative_id in adgroup.creative_ids:
            adcreatives.append(self.__fb.get_one_from_fb(creative_id, "AdCreative"))  # TODO: This should be a batch request
        return adcreatives

    def create(self, account_id, name=None, adcreative_type='25', object_id=None, body=None, image_hash=None, image_url=None, creative_id=None, count_current_adgroups=None, title=None, run_status=None, link_url=None, url_tags=None, preview_url=None, related_fan_page=None, follow_redirect=None, auto_update=None, story_id=None, action_spec=None):
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
        kwargs = {
            'account_id': account_id,
            'type': adcreative_type,
            'object_id': object_id,
            'body': body,
            'image_hash': image_hash,
            'image_url': image_url,
            'creative_id': creative_id,
            'count_current_adgroups': count_current_adgroups,
            'title': title,
            'run_status': run_status,
            'link_url': link_url,
            'url_tags': url_tags,
            'preview_url': preview_url,
            'related_fan_page': related_fan_page,
            'follow_redirect': follow_redirect,
            'auto_update': auto_update,
            'story_id': story_id,
            'action_spec': action_spec
        }
        kwargs = self.__fb.clean_params(**kwargs)
        model = self.__fb.create('AdCreative', **kwargs)
        return model

    def update(self, adcreative_id, **kwargs):
        """
        Updates an AdCreative given by it's id. Params to update depend on the type of adcreative.

        :param int adcreative_id The id of the AdCreative to update
        :param dict A dcitionary containing the key-value pairs of fields to update. The fields that may be updated depend on the type of AdCreative

        :rtype tuple The success status (i.e. True, None) of the process and the errors occured, if any.
        """
        kwargs = self.__fb.clean_params(**kwargs)
        result = self.__fb.update(adcreative_id, **kwargs)
        if result != True:
            return None
        return result

    def find_by_ids(self, adcreative_ids):
        """
        Retreives a list of AdCreative objects from a list of adcreative IDs subject to FB's max batch size/limit

        :param list adcreative_ids: The list of adcreative IDs we are searching for

        :rtype [AdCreative]: A list of AdCreative objects found.

        """
        return self.__fb.get_many_from_fb(adcreative_ids, 'AdCreative')
