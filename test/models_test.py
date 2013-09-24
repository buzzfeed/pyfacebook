import time
import unittest
import shelve
import anydbm
import inflection

from operator import itemgetter
from nose.tools import ok_, eq_
from tinymodel import TinyModel
from pprint import pprint

from pyfacebook import(
    settings,
    models,
    PyFacebook,
)

import post_fixtures

from pyfacebook.utils import(
    first_item,
    delete_shelf_files,
    json_to_objects,
)

anydbm._defaultmod = __import__('dumbdbm')


class FacebookModelsTest(unittest.TestCase):

    """
    Tests PyFacebook functionality for all Facebook models.
    If TEST_LIVE_ENDPOINTS is set to True, then this actually calls the Facebook Graph API.
    Otherwise, we use shelved data to mock out the endpoint calls.

    If you run this test with TEST_LIVE_ENDPOINTS set to True, then it will replace the current shelved data.

    """
    test_live_endpoints = settings.__dict__.get('TEST_LIVE_ENDPOINTS')
    limit_live_results = settings.__dict__.get('LIVE_TEST_RESULTSET_LIMIT')
    shelf_filename = str(__file__).split(".")[0]

    app_id = settings.__dict__.get('FACEBOOK_APP_ID')
    app_secret = settings.__dict__.get('FACEBOOK_APP_SECRET')
    test_token_text = settings.__dict__.get('FACEBOOK_TEST_ACCESS_TOKEN')
    account_id = settings.__dict__.get('FACEBOOK_TEST_ACCOUNT_ID')
    mock_account_id = settings.__dict__.get('MOCK_DATA_ACCOUNT_ID')

    if test_live_endpoints:
        print "TESTING LIVE ENDPOINTS WITH LIMIT", (limit_live_results or "INFINITE")
        if not(app_id and app_secret and test_token_text and account_id):
            raise Exception("MISSING SETTINGS FOR LIVE TEST!\n"
                            "FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_TEST_ACCESS_TOKEN\n"
                            "AND FACEBOOK_TEST_ACCOUNT_ID ALL NEED TO BE DEFINED!")
        account_id = account_id if account_id[0:4] == 'act_' else 'act_' + account_id
        delete_shelf_files(shelf_filename)
    else:
        if not(mock_account_id):
            raise Exception("MISSING SETTINGS FOR MOCK TEST: MOCK_DATA_ACCOUNT_ID NEEDS TO BE DEFINED")
        print "TESTING MOCK ENDPOINTS USING SHELVED DATA"
        account_id = mock_account_id if mock_account_id[0:4] == 'act_' else 'act_' + mock_account_id

    def setUp(self):
        """
        Set up models list, PyFacebook instance and shelf

        """
        get_models = [val for key, val in models.__dict__.items() if isinstance(val, type) and models.FacebookModel in val.__bases__]
        get_models.insert(0, get_models.pop(get_models.index(models.AdAccount)))
        self.get_models = get_models
        self.get_model_ids = {models.AdAccount: [self.account_id]}
        self.pyfb = PyFacebook(app_id=self.app_id, app_secret=self.app_secret, token_text=self.test_token_text)

        self.shelf = shelve.open(self.shelf_filename, protocol=-1)
        if self.test_live_endpoints:
            self.pyfb.put_on_shelf = self.shelf
        else:
            self.pyfb.get_from_shelf = self.shelf

    def tearDown(self):
        self.shelf.close()

    def __handle_results(self, results):
        """
        Validates a resultset, and appends valid models to get_model_ids.

        :param dict results: A resultset from PyFacebook.get

        """
        first_obj = first_item(results['data'])
        if first_obj and hasattr(first_obj, 'id'):
            first_obj.validate()
            self.get_model_ids[type(first_obj)] = [first_obj.id]
        return first_obj

    def __test_single_endpoint(self, model, http_method, id=None, connection=None, return_json=True, **kwargs):
        """
        Tests a single Facebook Ads endpoint

        :param FacebookModel model: The model returned by this endpoint
        :param str connection: The name of the connection, if we are testing one.

        """
        print "\n\n================"

        print "TESTING:"
        pprint(locals())
        shelf_key = str(id or model.__name__.lower()) + "__" + (connection or '') + "__" + http_method

        test_method = getattr(self.pyfb, http_method.lower())
        results = test_method(model=model, id=id, connection=connection, return_json=return_json, **kwargs)

        if return_json:
            results['data'] = json_to_objects(results['data'], model)
            return self.__handle_results(results)
        else:
            return results

    def __add_dependent_ids(self, dependent_fields, fixture_obj):
        """
        Adds ids and hashes of dependent objects to parent POST objects during live tests.

        :param dict dependent_fields: A dict of dependent field objects. See post_fixtures.py for an example.
        :param obj fixture_obj: The object we are testing, which we need to add dependent fields to

        """
        for field_name, dependent_model in dependent_fields.items():
            if isinstance(dependent_model, dict):
                for key, val in dependent_model.items():
                    dependent_obj = list(post_fixtures.FIXTURES[val].values())[0]
                    dependent_value = getattr(dependent_obj, 'id', None) or getattr(dependent_obj, 'hash')
                    setattr(fixture_obj, field_name, {key: dependent_value})
            else:
                dependent_obj = list(post_fixtures.FIXTURES[dependent_model].values())[0]
                dependent_value = getattr(dependent_obj, 'id', None) or getattr(dependent_obj, 'hash')
                setattr(fixture_obj, field_name, dependent_value)

    def test_exchange_access_token(self):
        """
        Test for the fb_exchange_token functionality of the /oauth/access_token endpoint

        """
        self.pyfb = PyFacebook(app_id=self.app_id, app_secret=self.app_secret, token_text=self.test_token_text)
        new_token = self.pyfb.exchange_access_token(current_token=self.pyfb.access_token, app_id=self.app_id, app_secret=self.app_secret)

    def test_graph_api(self):
        """
        Test for the POST, GET and DELETE functionality (in that order) of all defined FacebookModels and their connections.

        For POST:
        Models are posted to Facebook using the fixture data in post_fixtures

        For GET:
        AdAccount is gotten first, using FACEBOOK_TEST_ACCOUNT_ID as the id.
        Connected models are then gotten, using the ids from previous results.

        For DELETE:
        All POSTed objects are DELETEd.

        Due to the Facebook object hierarchy, POST tests go in this order:
        AdImage, AdCreative, AdGroup, AdCampaign

        """
        # test POST using fixtures
        for post_dict in post_fixtures.POST_MODELS:
            time.sleep(5)
            model = post_dict['model']
            for fixture_name, fixture_obj in post_fixtures.FIXTURES[model].items():
                # set ids or hashes of dependent objects if appropriate
                self.__add_dependent_ids(post_dict.get('dependent_fields', {}), fixture_obj)

                if hasattr(fixture_obj, 'file'):
                    post_params = {f.field_def.title: f.value for f in fixture_obj.FIELDS}
                else:
                    post_params = fixture_obj.to_json(return_dict=True)

                post_params.pop('id', None)
                post_params.pop('hash', None)
                connection = inflection.pluralize(model.__name__.lower())
                return_obj = self.__test_single_endpoint(model=model, http_method='POST', id=self.account_id, connection=connection, **post_params)
                if hasattr(return_obj, 'id'):
                    fixture_obj.id = return_obj.id
                elif hasattr(return_obj, 'hash'):
                    fixture_obj.hash = return_obj.hash

        # test GET starting with AdAccount and using first result from each successive return
        for model in self.get_models:
            if model not in self.get_model_ids.keys():
                print "\n\n==== SKIPPING GET TEST! NO TEST ID FOR", model.__name__, "===="
            else:
                for id in self.get_model_ids[model]:
                    self.__test_single_endpoint(model=model, http_method='GET', id=id, limit=self.limit_live_results)
                    for connection in getattr(model, 'CONNECTIONS', []):
                        connection_field_def = next(f for f in model.FIELD_DEFS if f.title == connection)
                        child_model = first_item(connection_field_def.allowed_types[0])
                        self.__test_single_endpoint(model=child_model, http_method='GET', id=id, connection=connection, limit=self.limit_live_results)

        # test DELETE by deleting posted models from above
        post_fixtures.POST_MODELS.reverse()
        for post_dict in post_fixtures.POST_MODELS:
            model = post_dict['model']
            for fixture_name, fixture_obj in post_fixtures.FIXTURES[model].items():
                if hasattr(fixture_obj, 'id'):
                    ok_(self.__test_single_endpoint(model=model, id=fixture_obj.id, http_method='DELETE', return_json=False))
