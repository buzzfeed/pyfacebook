import random
from pyfacebook.settings import (
    FACEBOOK_PROD_ACCOUNT_ID,
    FACEBOOK_TEST_ACCOUNT_ID
)


ADACCOUNT = {
    "id": "act_%s" % FACEBOOK_TEST_ACCOUNT_ID,
    "account_id": str(FACEBOOK_TEST_ACCOUNT_ID),
    "name": "BuzzFeed RnD_API Testing",
    "account_status": 1,
    "timezone_name": "America/Los_Angeles",
    "currency": "USD"
}
ADCAMPAIGN = {
    "id": "",
    "account_id": FACEBOOK_PROD_ACCOUNT_ID,
    "name": "fixture_name | fixture",
    "end_time": "2013-11-16T14:58:59-0700",
}
ADCREATIVE = {
    "id": "",
    "body": "This is a mock object",
    "name": "fixture_name-",
    "link_url": "http://www.example.com",
    "title": "fixture_title",
    "type": "fixture",
    # "action_spec": json.dumps({"action.type":["flightsim:fly"], "application":[123456789]}),
    "action_spec": None,
}
ADGROUP = {
    "id": "",
    "ad_id": random.randint(1, 1000),
    "name": "fixture",
    "campaign_id": random.randint(1, 1000),
    "adgroup_id": random.randint(1, 1000),
    "creative_ids": [1, 2, 3, 4],
}
ADSTATISTIC = {
    "id": "",
    "social_unique_clicks": 123,
    "unique_impressions": 1234,
    "social_clicks": 12345678,
    "social_impressions": 12345,
    "social_unique_impressions": 2,
    "social_spent": 800,
    "impressions": 1000,
    "clicks": 1,
    "unique_clicks": 123456,
}
ADUSER = {
    "id": "",
    "role": 105,
    "adaccounts": [1, 2, 3, 4],
}
BROADTARGETINGCATEGORY = {
    "id": "",
    "name": "Fixture_title",
    "parent_category": "Custom",
    "size": 1234,
}
