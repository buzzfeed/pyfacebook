import random
import pytz
import datetime
import calendar
from tinymodel import TinyModel, FieldDef

unix_datetime_translators = {
    'to_json': lambda obj: calendar.timegm(datetime.datetime.utcfromtimestamp(obj.utctimetuple())),
    'from_json': lambda json_value: datetime.datetime.utcfromtimestamp(long(json_value)),
    'random': lambda: (datetime.datetime.utcnow() - datetime.timedelta(seconds=random.randrange(2592000))).replace(tzinfo=pytz.utc),
}


class FacebookModel(TinyModel):

    """
    Represents a model defined by Facebook. See documentation at:
    https://developers.facebook.com/docs/ads-api/

    There should be a 1-to-1 correspondence to the Facebook model definitions,
    with the notable exception of "connections" which we defined as model fields but Facebook does not.

    """
    endpoint = None


class SupportModel(TinyModel):

    """
    Represents models which Facebook uses, but do not have their own endpoints.
    These models generally don't have their own page in the Facebook documentation,
    but are mentioned or implied in the documentation of other models.

    """
    pass


class Token(SupportModel):

    """
    Represents an oauth token for the Facebook Graph API.
    Fields are taken mostly from the return structure of the debug_token call documented at:
    https://developers.facebook.com/docs/facebook-login/access-tokens/#debug

    """
    FIELD_DEFS = [
        FieldDef(title='text', allowed_types=[unicode]),
        FieldDef(title='app_id', allowed_types=[unicode]),
        FieldDef(title='is_valid', allowed_types=[bool]),
        FieldDef(title='application', allowed_types=[unicode]),
        FieldDef(title='user_id', allowed_types=[unicode]),
        FieldDef(title='issued_at', allowed_types=[datetime.datetime], custom_translators=unix_datetime_translators),
        FieldDef(title='expires_at', allowed_types=[datetime.datetime], custom_translators=unix_datetime_translators),
        FieldDef(title='scopes', allowed_types=[[unicode], [unicode]]),
    ]


class AdImage(FacebookModel):

    """
    Represents an adimage object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adimage/

    """
    FIELD_DEFS = [
        FieldDef(title='hash', allowed_types=[unicode]),
        FieldDef(title='url', allowed_types=[unicode]),
        FieldDef(title='file', allowed_types=[{unicode: file}], validate=False),
    ]

    CREATE_ONLY = ['file']


class AdUser(FacebookModel):

    """
    Represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/aduser/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='permissions', allowed_types=[[int]]),
        FieldDef(title='role', allowed_types=[int], choices=[1001, 1002, 1003]),
    ]

    CREATE_ONLY = ['role']


class AdStatistic(FacebookModel):

    """
    Represents an adstatistic objects in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adstatistics

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='adcampaign_id', allowed_types=[long]),
        FieldDef(title='adgroup_id', allowed_types=[long]),
        FieldDef(title='impressions', allowed_types=[int]),
        FieldDef(title='clicks', allowed_types=[int]),
        FieldDef(title='spent', allowed_types=[int]),
        FieldDef(title='social_impressions', allowed_types=[int]),
        FieldDef(title='social_clicks', allowed_types=[int]),
        FieldDef(title='social_spent', allowed_types=[int]),
        FieldDef(title='unique_impressions', allowed_types=[int]),
        FieldDef(title='unique_clicks', allowed_types=[int]),
        FieldDef(title='social_unique_impressions', allowed_types=[int]),
        FieldDef(title='social_unique_clicks', allowed_types=[int]),
        FieldDef(title='start_time', allowed_types=[datetime.datetime, type(None)]),
        FieldDef(title='end_time', allowed_types=[datetime.datetime, type(None)]),
    ]


class BroadTargetingCategory(SupportModel):

    """
    Represents the broadtargetingcategory object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='parent_category', allowed_types=[unicode, type(None)]),
        FieldDef(title='size', allowed_types=[int]),
        FieldDef(title='type', allowed_types=[int]),
        FieldDef(title='type_name', allowed_types=[unicode]),
    ]


class Region(SupportModel):

    """
    Represents a region for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class Country(SupportModel):

    """
    Represents a country for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='country_code', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='supports_region', allowed_types=[bool]),
        FieldDef(title='supports_city', allowed_types=[bool]),
    ]


class City(SupportModel):

    """
    Represents a city for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class CollegeNetwork(SupportModel):

    """
    Represents a college network for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class WorkNetwork(SupportModel):

    """
    Represents a work network for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class UserConnection(SupportModel):
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class CustomAudience(FacebookModel):

    """
    Represents the customaudience object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/custom-audience-targeting
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='approximate_count', allowed_types=[int]),
    ]


class Targeting(SupportModel):

    """
    Represents a targeting object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='genders', allowed_types=[[int]], choices=[[1], [2], [1, 2]]),
        FieldDef(title='age_min', allowed_types=[int]),
        FieldDef(title='age_max', allowed_types=[int]),
        FieldDef(title='broad_age', allowed_types=[int], choices=[0, 1]),
        FieldDef(title='geo_locations', allowed_types=[
            {str: [City]},  # cities
            {str: str},  # zipcodes
            {str: [Region]},  # regions
            [str]  # countries
        ]),
        FieldDef(title='user_adclusters', allowed_types=[[BroadTargetingCategory]]),
        FieldDef(title='excluded_user_adclusters', allowed_types=[[BroadTargetingCategory]]),
        FieldDef(title='keywords', allowed_types=[[unicode]]),
        FieldDef(title='interests', allowed_types=[[dict]]),
        FieldDef(title='user_os', allowed_types=[[unicode]]),
        FieldDef(title='user_device', allowed_types=[[unicode]], choices=['iPhone', 'iPod', 'android_tablet', 'android_smartphone']),
        FieldDef(title='wireless_carrier', allowed_types=[[unicode]], choices=['WiFi']),
        FieldDef(title='site_category', allowed_types=[[unicode]], choices=['feature_phones']),
        FieldDef(title='connections', allowed_types=[[UserConnection]]),
        FieldDef(title='excluded_connections', allowed_types=[[UserConnection]]),
        FieldDef(title='friends_of_connections', allowed_types=[[UserConnection]]),
        FieldDef(title='college_networks', allowed_types=[[CollegeNetwork]]),
        FieldDef(title='work_networks', allowed_types=[[WorkNetwork]]),
        FieldDef(title='custom_audiences', allowed_types=[[CustomAudience]]),
        FieldDef(title='education_statuses', allowed_types=[[int]], choices=[[1], [2], [3]]),
        FieldDef(title='college_majors', allowed_types=[[unicode]]),
        FieldDef(title='page_types', allowed_types=[[unicode]], choices=[['desktop'], ['feed'], ['desktopfeed'], ['mobile'], ['rightcolumn'], ['home'], ['mobile-and-external']]),
        FieldDef(title='relationship_statuses', allowed_types=[[int]]),
        FieldDef(title='interested_in', allowed_types=[[int]], choices=[[1], [2]]),
        FieldDef(title='locales', allowed_types=[{unicode: unicode, unicode: unicode}, [unicode]]),
        FieldDef(title='ethnic_affinity', allowed_types=[{unicode: unicode, unicode: unicode}]),
    ]


class ActionSpec(SupportModel):

    """
    Represents the actionspec object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/action-specs/

    Currently this supports ONLY on-site objects and actions

    """
    FIELD_DEFS = [
        FieldDef(title='action.type', allowed_types=[[unicode]]),
        FieldDef(title='applicaton', allowed_types=[[long]]),
        FieldDef(title='offer', allowed_types=[[long]]),
        FieldDef(title='event', allowed_types=[[long]]),
        FieldDef(title='question', allowed_types=[[long]]),
        FieldDef(title='page', allowed_types=[[long]]),
        FieldDef(title='post', allowed_types=[[long]]),
    ]


class TrackingSpec(SupportModel):

    """
    Represents the trackingspec object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/tracking-specs

    """
    FIELD_DEFS = [
        FieldDef(title='action.type', allowed_types=[[unicode]]),
        FieldDef(title='page', allowed_types=[[long]]),
        FieldDef(title='application', allowed_types=[[long]]),
        FieldDef(title='object', allowed_types=[[unicode]]),
        FieldDef(title='object.domain', allowed_types=[[unicode]]),
        FieldDef(title='post', allowed_types=[[long]]),
        FieldDef(title='post.wall', allowed_types=[[long]]),
        FieldDef(title='offer', allowed_types=[[long]]),
    ]


class AdPreviewCss(FacebookModel):

    """
    Represents the AdPreview Css object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/generatepreview/#adpreviewcss
    """
    FIELD_DEFS = [
        FieldDef(title='result', allowed_types=[unicode]),
    ]


class Preview(FacebookModel):

    """
    Represents the Preview object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/generatepreview/
    """
    FIELD_DEFS = [
        FieldDef(title='body', allowed_types=[unicode]),
    ]


class AdCreative(FacebookModel):

    """
    Represents the adcreative object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcreative

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='type', allowed_types=[int], choices=[1, 2, 3, 4, 12, 25, 27]),
        FieldDef(title='object_id', allowed_types=[long]),
        FieldDef(title='object_story_id', allowed_types=[unicode]),
        FieldDef(title='object_url', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='title', allowed_types=[unicode]),
        FieldDef(title='body', allowed_types=[unicode]),
        FieldDef(title='image_hash', allowed_types=[unicode, type(None)]),
        FieldDef(title='image_url', allowed_types=[unicode]),
        FieldDef(title='link_url', allowed_types=[unicode]),
        FieldDef(title='preview_url', allowed_types=[unicode]),
        FieldDef(title='url_tags', allowed_types=[unicode]),
        FieldDef(title='related_fan_page', allowed_types=[long]),
        FieldDef(title='story_id', allowed_types=[long]),
        FieldDef(title='follow_redirect', allowed_types=[bool]),
        FieldDef(title='auto_update', allowed_types=[bool]),
        FieldDef(title='action_spec', allowed_types=[[ActionSpec]]),
        FieldDef(title='previews', allowed_types=[[Preview]]),
    ]

    CREATE_ONLY = ['follow_redirect']
    CONNECTIONS = ['previews']


class AdGroup(FacebookModel):

    """
    Represents an adgroup object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adgroup

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='account_id', allowed_types=[int]),
        FieldDef(title='campaign_id', allowed_types=[long, int]),
        FieldDef(title='adgroup_status', allowed_types=[unicode], choices=['ACTIVE', 'DELETED', 'PENDING_REVIEW', 'DISAPPROVED', 'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'PAUSED']),
        FieldDef(title='adgroup_review_feedback', allowed_types=[unicode]),
        FieldDef(title='bid_type', allowed_types=[unicode], choices=['CPC', 'CPM', 'MULTI_PREMIUM', 'RELATIVE_OCPM', 'ABSOLUTE_OCPM', 'CPA']),
        FieldDef(title='bid_info', allowed_types=[{unicode: int}, type(None)]),
        FieldDef(title='creative_ids', allowed_types=[[long]]),
        FieldDef(title='creative', allowed_types=[{unicode: long}]),
        FieldDef(title='targeting', allowed_types=[Targeting, type(None)]),
        FieldDef(title='tracking_specs', allowed_types=[[TrackingSpec]]),
        FieldDef(title='last_updated_by_app_id', allowed_types=[long, int]),
        FieldDef(title='created_time', allowed_types=[datetime.datetime]),
        FieldDef(title='updated_time', allowed_types=[datetime.datetime]),
        FieldDef(title='stats', allowed_types=[[AdStatistic]]),
        FieldDef(title='adcreatives', allowed_types=[[AdCreative]]),
        FieldDef(title='previews', allowed_types=[[Preview]]),
    ]

    CREATE_ONLY = ['creative']
    CONNECTIONS = ['stats', 'adcreatives', 'previews']


class AdCampaignGroup(FacebookModel):
    endpoint = 'adcampaign_groups'
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='objective', allowed_types=[unicode]),
        FieldDef(title='campaign_group_status', allowed_types=[unicode]),
        FieldDef(title='buying_type', allowed_types=[unicode]),
    ]


class AdSet(FacebookModel):

    """
    Represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcampaign/

    """
    endpoint = 'adcampaigns'
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='campaign_group_id', allowed_types=[long]),
        FieldDef(title='start_time', allowed_types=[datetime.datetime]),
        FieldDef(title='end_time', allowed_types=[datetime.datetime]),
        FieldDef(title='created_time', allowed_types=[datetime.datetime]),
        FieldDef(title='updated_time', allowed_types=[datetime.datetime]),
        FieldDef(title='daily_budget', allowed_types=[int]),
        FieldDef(title='lifetime_budget', allowed_types=[int]),
        FieldDef(title='budget_remaining', allowed_types=[int]),
        FieldDef(title='campaign_status', allowed_types=[unicode], choices=['ACTIVE', 'PAUSED']),
        FieldDef(title='adcreatives', allowed_types=[[AdCreative]]),
        FieldDef(title='adgroups', allowed_types=[[AdGroup]]),
        FieldDef(title='stats', allowed_types=[[AdStatistic]]),
    ]

    CONNECTIONS = ['adcreatives', 'adgroups', 'stats']


class AdAccount(FacebookModel):

    """
    Represents the adaccount object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adaccount/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='account_status', allowed_types=[int]),
        FieldDef(title='currency', allowed_types=[unicode]),
        FieldDef(title='timezone_id', allowed_types=[int]),
        FieldDef(title='timezone_name', allowed_types=[unicode]),
        FieldDef(title='timezone_offset_hours_utc', allowed_types=[int]),
        FieldDef(title='daily_spend_limit', allowed_types=[int]),
        FieldDef(title='amount_spent', allowed_types=[int]),
        FieldDef(title='users', allowed_types=[[AdUser]]),
        FieldDef(title='adcampaigns', allowed_types=[[AdSet]]),
        FieldDef(title='adimages', allowed_types=[[AdImage]]),
        FieldDef(title='adcreatives', allowed_types=[[AdCreative]]),
        FieldDef(title='adgroups', allowed_types=[[AdGroup]]),
        FieldDef(title='stats', allowed_types=[[AdStatistic]]),
        FieldDef(title='adgroupstats', allowed_types=[[AdStatistic]]),
        FieldDef(title='customaudiences', allowed_types=[[CustomAudience]]),
        FieldDef(title='adpreviewscss', allowed_types=[[AdPreviewCss]]),
    ]

    CONNECTIONS = ['users', 'adcampaigns', 'adimages', 'adcreatives',
                   'adgroups', 'stats', 'adgroupstats', 'adpreviewscss', 'customaudiences']


class Post(FacebookModel):
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='message', allowed_types=[unicode]),
        FieldDef(title='picture', allowed_types=[unicode, type(None)]),
        FieldDef(title='link', allowed_types=[unicode, type(None)]),
        FieldDef(title='published', allowed_types=[bool]),
    ]
