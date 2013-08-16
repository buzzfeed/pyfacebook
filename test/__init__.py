import random
from . import fixtures
from nose.tools import eq_, ok_, set_trace
from pyfacebook import PyFacebook
from pyfacebook.settings import (
    FACEBOOK_APP_SECRET,
    FACEBOOK_APP_ID,
    FACEBOOK_TEST_ACCESS_TOKEN,
    FACEBOOK_PROD_ACCOUNT_ID,
    FACEBOOK_TEST_ACCOUNT_ID
)


class ApiTest(object):
    def __init__(self, *args, **kwargs):
        self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                             access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                             app_secret=FACEBOOK_APP_SECRET)
        super(ApiTest, self).__init__(*args, **kwargs)
        self.ok_ = ok_
        self.eq_ = eq_
        self.set_trace = set_trace
        self.FACEBOOK_PROD_ACCOUNT_ID = FACEBOOK_PROD_ACCOUNT_ID
        self.FACEBOOK_TEST_ACCOUNT_ID = FACEBOOK_TEST_ACCOUNT_ID

    def setUp(self, apis=[]):
        for api_ in apis:
            api_name = api_.__name__.lower() + '_api'
            setattr(self, api_name, api_(fb=self.fb))

    def get_patch_kwargs(self, api, get_many=False, number=None, nest_by_id=False):
        """
        Retrieves the settings used to replace the output of the function to patch.

        :param pyfacebook.api.Model api: The API to get the fixture for.
        :param bool get_many: Indicates whether to retrieve several objects with random Indicates
        :param int number: A fixed number of objects to retrieve.
        :param bool nest_by_id: Whether to avoid putting the objects in a "data" key within the response.

        :rtype dict: The settings dictionary.
        """
        return {
            '__name__': '_json_response',
            'return_value': self.get_mock_fb_response(api, get_many=get_many, number=number, nest_by_id=nest_by_id)
        }

    def get_mock_fb_response(self, api, get_many=False, number=None, nest_by_id=False):
        """
        Retrieves a fake fixture output based on the given API.

        :param pyfacebook.api.Model api: The API to get the fixture for.
        :param bool get_many: Indicates whether to retrieve several objects with random Indicates
        :param int number: A fixed number of objects to retrieve.
        :param bool nest_by_id: Whether to avoid putting the objects in a "data" key within the response.

        :rtype dict: The generated object or dictionary containing the list of generated objects.
        """
        fixture = getattr(fixtures, api.__name__.upper()).copy()
        if number == 0:
            return {} if nest_by_id else {'data': []}
        if number or get_many:
            number = number or random.randint(1, 10)
            if 'id' in fixture and not fixture['id'].startswith('act_'):
                fixture_list = []
                for idx in xrange(1, number + 1):
                    f = fixture.copy()
                    f['id'] = str(idx)
                    fixture_list.append(f)
            else:
                fixture_list = [fixture] * number
            if nest_by_id:
                return dict(map(lambda o: (o['id'], o), fixture_list))
            return {"data": fixture_list}
        else:
            f = fixture
            if 'id' in fixture and not fixture['id'].startswith('act_'):
                fixture['id'] = str(1)
            return fixture
