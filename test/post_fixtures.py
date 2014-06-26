import os
import datetime
import pytz
from pyfacebook import models as m

MY_DIR = os.path.dirname(os.path.realpath(__file__))

# This list stores the order in which models should be tested for POST
# Order matters because some models contain others
POST_MODELS = [
    {'model': m.AdCampaignGroup},
    {'model': m.AdSet,
     'dependent_fields': {'campaign_group_id': m.AdCampaignGroup}
    },
    {'model': m.AdImage},
    {'model': m.AdGroup,
     'dependent_fields': {'creative': {'creative_id': m.AdCreative}, 'campaign_id': m.AdSet}
     },
]

test_targeting = m.Targeting(**{
    'genders': [1],
    'age_min': 18,
    'age_max': 50,
    'broad_age': 1,
    'geo_locations': {
        'countries': ['GB'],
        'cities': [m.City(**{'id': '2421215', 'name': 'Palo Alto, CA'}),
                   m.City(**{'id': '220522764', 'name': 'Dublin, OH'})],
        'regions': [m.Region(**{'id': '1', 'name': 'Alabama'}),
                    m.Region(**{'id': '2', 'name': 'Alaska'})],
    },
    'user_adclusters': [m.BroadTargetingCategory(**{'id': 6002714886772, 'name': 'Food & Dining'}),
                                    m.BroadTargetingCategory(**{'id': 6002714885172, 'name': 'Cooking'})],
    'excluded_user_adclusters': [m.BroadTargetingCategory(**{'id': 6002714898572, 'name': 'Small Business Owners'})],
    'interests': ['movies', '#Red Bull'],
    'connections': [m.UserConnection(**{'id': '481523265256333', 'name': 'Discotech'})],
    'excluded_connections': [m.UserConnection(**{'id': '481523265256333', 'name': 'Discotech'})],
    'friends_of_connections': [m.UserConnection(**{'id': '481523265256333', 'name': 'Discotech'})],
    'college_networks': [m.CollegeNetwork(**{'id': '16777217', 'name': 'Harvard'}),
                         m.CollegeNetwork(**{'id': '16777445', 'name': 'Hartford'})],
    'work_networks': [m.WorkNetwork(**{'id': '50431654', 'name': 'Microsoft'}),
                      m.WorkNetwork(**{'id': '50446992', 'name': 'MindShare'})],
    'education_statuses': [3],
    'college_majors': ['Mathematics', 'English'],
    'ad_format': ['DESKTOP_FEED_STANDARD'],
    'relationship_statuses': [1, 2, 3],
    'interested_in': [1],
    'locales': [6, 24, 51],
})


FIXTURES = {}

# Fixtures need dummy id's until they are populated with real values!
FIXTURES[m.AdCampaignGroup] = {
    'test_campaign_group':
    m.AdCampaignGroup(**{
        'name': 'test_campaign_group',
        'objective': 'WEBSITE_CLICKS',
        'campaign_group_status': 'PAUSED',
    })
}

FIXTURES[m.AdSet] = {
    'test_campaign':
    m.AdSet(**{
                 'name': 'test_campaign',
                 'campaign_status': 'ACTIVE',
                 'lifetime_budget': 100,
                 'start_time': datetime.datetime(2014, 10, 1).replace(tzinfo=pytz.utc),
                 'end_time': datetime.datetime(2014, 10, 2).replace(tzinfo=pytz.utc),
                 }),
}

FIXTURES[m.AdImage] = {
    'test_image':
    m.AdImage(**{
              'file': {'test_image.png': open(MY_DIR + '/test_image.png', 'r').read()},
              }),
}

FIXTURES[m.AdCreative] = {
    'domain_ad_creative':
    m.AdCreative(**{
        'title': 'domain_ad_creative',
        'body': 'domain ad creative body',
        'object_url': 'http://www.buzzfeed.com',
        'related_fan_page': 572030329512884,
    }),
    'page_like_ad_creative':
    m.AdCreative(**{
        'body': 'page like ad creative body',
        'object_id': 572030329512884,
    }),
    'event_ad_creative':
    m.AdCreative(**{
        'object_id': 481523265256333,
        'body': 'event ad creative body',
        'name': 'event_ad_creative',
        'title': 'event_ad_creative title',
    }),
    'page_post_ad_creative':
    m.AdCreative(**{
        'object_story_id': '572030329512884_10202995793919333'
    }),
    'type_27_test_creative':
    m.AdCreative(**{
        'object_id': 572030329512884,
        'image_hash': '1d8141f49fddc410dcec70c7c620f931'
    })
}

FIXTURES[m.AdGroup] = {
    'test_adgroup':
    m.AdGroup(**{
        'name': 'test_adgroup',
        'bid_type': 'CPM',
        'bid_info': {'IMPRESSIONS': 2},
        'targeting': test_targeting,
    }),
}
