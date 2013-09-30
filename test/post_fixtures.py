import os
import random
import datetime
import pytz
from pyfacebook import models as m

MY_DIR = os.path.dirname(os.path.realpath(__file__))

# This list stores the order in which models should be tested for POST
# Order matters because some models contain others
POST_MODELS = [
    {'model': m.AdCampaign},
    {'model': m.AdImage},
    {'model': m.AdCreative,
     'dependent_fields': {'image_hash': m.AdImage}
     },
    {'model': m.AdGroup,
     'dependent_fields': {'creative': {'creative_id': m.AdCreative}, 'campaign_id': m.AdCampaign}
     },
]

test_targeting = m.Targeting(**{
    'genders': [1],
    'age_min': 18,
    'age_max': 50,
    'broad_age': 1,
    'countries': ['US', 'GB'],
    'cities': [m.City(**{'id': '2421215', 'name': 'Palo Alto, CA'}),
               m.City(**{'id': '220522764', 'name': 'Dublin, OH'})],
    'regions': [m.Region(**{'id': '1', 'name': 'Alabama'}),
                m.Region(**{'id': '2', 'name': 'Alaska'})],
    'radius': 10.5,
    'conjunctive_user_adclusters': [m.BroadTargetingCategory(**{'id': 6002714886772, 'name': 'Food & Dining'}),
                                    m.BroadTargetingCategory(**{'id': 6002714885172, 'name': 'Cooking'})],
    'excluded_user_adclusters': [m.BroadTargetingCategory(**{'id': 6002714898572, 'name': 'Small Business Owners'})],
    'keywords': ['movies', '#Red Bull'],
    'college_networks': [m.CollegeNetwork(**{'id': '16777217', 'name': 'Harvard'}),
                         m.CollegeNetwork(**{'id': '16777445', 'name': 'Hartford'})],
    'work_networks': [m.WorkNetwork(**{'id': '50431654', 'name': 'Microsoft'}),
                      m.WorkNetwork(**{'id': '50446992', 'name': 'MindShare'})],
    'education_statuses': [3],
    'college_majors': ['Mathematics', 'English'],
    'page_types': ['desktop'],
    'relationship_statuses': [1, 2, 3],
    'interested_in': [1],
    'locales': [6, 24, 51],
})


FIXTURES = {}

# Fixtures need dummy id's until they are populated with real values!
FIXTURES[m.AdCampaign] = {
    'test_campaign':
    m.AdCampaign(**{
                 'name': 'test_campaign',
                 'campaign_status': 2,
                 'lifetime_budget': 100,
                 'start_time': datetime.datetime.today().replace(tzinfo=pytz.utc) + datetime.timedelta(days=30),
                 'end_time': datetime.datetime.today().replace(tzinfo=pytz.utc) + datetime.timedelta(days=31),
                 }),
}


FIXTURES[m.AdImage] = {
    'test_image':
    m.AdImage(**{
              'file': {'test_image.png': open(MY_DIR + '/test_image.png', 'r')},
              }),
}

FIXTURES[m.AdCreative] = {
    'type_1_test_creative':
    m.AdCreative(**{
                 'type': 1,
                 'name': 'test_type_1_creative_name',
                 'title': 'type 1 creative title',
                 'body': 'test type 1 creative body',
                 'link_url': 'http://www.buzzfeed.com',
                 'related_fan_page': 238205562866018,
                 }),
    'type_2_test_creative':
    m.AdCreative(**{
                 'type': 2,
                 'name': 'test_type_2_creative_name',
                 'title': 'type 2 creative title',
                 'body': 'test type 2 creative body',
                 'object_id': 238205562866018,
                 }),
    'type_12_test_creative':
    m.AdCreative(**{
                 'type': 12,
                 'name': 'test_type_12_creative_name',
                 'title': 'type 12 creative title',
                 'body': 'test type 12 creative body',
                 'link_url': 'http://buzzfeed.com',
                 'object_id': 481523265256333,
                 }),
    'type_25_test_creative':
    m.AdCreative(**{
                 'type': 25,
                 'name': 'test_type_25_creative_name',
                 'url_tags': 'foo=bar&bat=baz',
                 'object_id': 238205562866018,
                 'action_spec': [m.ActionSpec(**{'action.type': ['like'], 'post': [609718625714708]})],
                 }),
    'type_27_test_creative':
    m.AdCreative(**{
                 'type': 27,
                 'name': 'test_type_27_creative_name',
                 'url_tags': 'foo=bar&bat=baz',
                 'object_id': 238205562866018,
                 'story_id': 609720135714557,
                 }),
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
