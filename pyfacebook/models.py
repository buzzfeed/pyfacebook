import random
import pytz
import datetime
import calendar
from tinymodel import TinyModel, FieldDef

unix_datetime_translators = {'to_json': lambda obj: calendar.timegm(utcfromtimestamp(obj.utctimetuple())),
                             'from_json': lambda json_value: datetime.datetime.utcfromtimestamp(long(json_value)),
                             'random': lambda: (datetime.datetime.utcnow() - timedelta(seconds=random.randrange(2592000))).replace(tzinfo=pytz.utc),
                            }

class Token(TinyModel):
    FIELD_DEFS = [
        FieldDef(title='text', allowed_types=[unicode, str]),
        FieldDef(title='app_id', allowed_types=[unicode, str]),
        FieldDef(title='is_valid', allowed_types=[bool]),
        FieldDef(title='application', allowed_types=[unicode, str]),
        FieldDef(title='user_id', allowed_types=[unicode, str]),
        FieldDef(title='issued_at', allowed_types=[datetime.datetime], custom_translators=unix_datetime_translators),
        FieldDef(title='expires_at', allowed_types=[datetime.datetime], custom_translators=unix_datetime_translators),
        FieldDef(title='scopes', allowed_types=[[unicode], [str]]),
    ]

class ActionSpec(TinyModel):
    """
    The ActionSpec class represents the action-spec object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/action-specs/
    We extend the functionality in the documentation with custom calls for action-specs
    """
    FIELD_DEFS = [
        FieldDef(title='action.type', allowed_types=[[unicode], type(None)]),
        FieldDef(title='post', allowed_types=[unicode]),
        FieldDef(title='post.object', allowed_types=[unicode, type(None)]),
    ]

class AdCampaign(TinyModel):
    """
    The AdCampaign class represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcampaign/
    We extend the functionality in the documentation with custom calls for adcampaigns
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[str]),
        FieldDef(title='start_time', allowed_types=[int, unicode]),
        FieldDef(title='end_time', allowed_types=[int, unicode]),
        FieldDef(title='daily_budget', allowed_types=[int]),
        FieldDef(title='campaign_status', allowed_types=[int]),
        FieldDef(title='lifetime_budget', allowed_types=[int]),
    ]

class AdStatistic(TinyModel):
    """
    The AdStatistic class represents an adstatistic objects in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adstatistics
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[str]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='start_time', allowed_types=[str]),
        FieldDef(title='end_time', allowed_types=[str]),
        FieldDef(title='impressions', allowed_types=[unicode]),
        FieldDef(title='clicks', allowed_types=[unicode]),
        FieldDef(title='spent', allowed_types=[unicode]),
        FieldDef(title='social_impressions', allowed_types=[unicode]),
        FieldDef(title='social_clicks', allowed_types=[unicode]),
        FieldDef(title='social_spent', allowed_types=[unicode]),
        FieldDef(title='unique_impressions', allowed_types=[unicode]),
        FieldDef(title='unique_clicks', allowed_types=[unicode]),
        FieldDef(title='social_unique_impressions', allowed_types=[int]),
        FieldDef(title='social_unique_clicks', allowed_types=[unicode]),
    ]

class Targeting(TinyModel):
    """
    The Targeting class represents an targeting object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/
    """
    FIELD_DEFS = [
        FieldDef(title='genders', allowed_types=[[int]]),
        FieldDef(title='age_min', allowed_types=[int]),
        FieldDef(title='age_max', allowed_types=[int]),
        FieldDef(title='broad_age', allowed_types=[int]),
        FieldDef(title='countries', allowed_types=[[unicode]]),
        FieldDef(title='cities', allowed_types=[[unicode]]),
        FieldDef(title='regions', allowed_types=[[unicode]]),
        FieldDef(title='radius', allowed_types=[int]),
        FieldDef(title='keywords', allowed_types=[[unicode]]),
    ]

class AdCreative(TinyModel):
    """
    The AdCreative class represents the adcreative object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcreative
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='body', allowed_types=[unicode]),
        FieldDef(title='link_url', allowed_types=[unicode]),
        FieldDef(title='title', allowed_types=[unicode]),
        FieldDef(title='action_spec', allowed_types=[[ActionSpec], type(None)]),
        FieldDef(title='type', allowed_types=[unicode]),
    ]

class AdUser(TinyModel):
    """
    The AdUser class represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/aduser/
    We extend the functionality in the documentation with custom calls for adaccounts
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='role', allowed_types=[int]),
    ]

class BroadTargetingCategory(TinyModel):
    """
    The BroadTargetingCategory class represents the broadtargetingcategory object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/
    We extend the functionality in the documentation with custom calls for adaccounts
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[int]),
        FieldDef(title='name', allowed_types=[str]),
        FieldDef(title='parent_category', allowed_types=[str]),
        FieldDef(title='size', allowed_types=[int]),
    ]

class AdGroup(TinyModel):
    """
    The AdGroup class represents an adgroup object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adgroup
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='campaign_id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[str]),
        FieldDef(title='disapprove_reason_descriptions', allowed_types=[str]),
        FieldDef(title='adgroup_status', allowed_types=[int]),
        FieldDef(title='ad_status', allowed_types=[int]),
        FieldDef(title='bid_info', allowed_types=[{str: int}, type(None)]),
        FieldDef(title='bid_type', allowed_types=[int]),
        FieldDef(title='updated_time', allowed_types=[int, unicode]),
        FieldDef(title='account_id', allowed_types=[int]),
        FieldDef(title='targeting', allowed_types=[Targeting, type(None)]),
        FieldDef(title='creative_ids', allowed_types=[[int]]),
    ]

class AdAccount(TinyModel):
    """
    The AdAccount class represents the adaccount object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adaccount/
    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[str]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='account_status', allowed_types=[int]),
        FieldDef(title='currency', allowed_types=[str]),
        FieldDef(title='timezone_id', allowed_types=[int]),
        FieldDef(title='timezone_name', allowed_types=[str]),
        FieldDef(title='vat_status', allowed_types=[int]),
        FieldDef(title='daily_spend_limit', allowed_types=[int]),
        FieldDef(title='amount_spent', allowed_types=[int]),
        FieldDef(title='adgroups', allowed_types=[AdGroup, type(None)]),
        FieldDef(title='users', allowed_types=[[AdUser], type(None)]),
        FieldDef(title='stats', allowed_types=[[AdStatistic], type(None)]),
        FieldDef(title='broadtargetingcategories', allowed_types=[[BroadTargetingCategory], type(None)]),
    ]

