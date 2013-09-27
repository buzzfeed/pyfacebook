import unittest
import shelve
import anydbm

from operator import itemgetter
from nose.tools import ok_, eq_
from tinymodel import TinyModel
from pprint import pprint

from pyfacebook import settings
from pyfacebook import models
from pyfacebook import PyFacebook
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
            raise Exception("MISSING SETTINGS FOR LIVE TEST! "
                            "FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_TEST_ACCESS_TOKEN "
                            "AND FACEBOOK_TEST_ACCOUNT_ID ALL NEED TO BE DEFINED!")
        delete_shelf_files(shelf_filename)
    else:
        print "TESTING MOCK ENDPOINTS USING SHELVED DATA"
        account_id = mock_account_id

    def setUp(self):
        """
        Set up list of test_models and test_model_ids

        """
        self.shelf = shelve.open(self.shelf_filename)
        test_models = [val for key, val in models.__dict__.items() if isinstance(val, type) and models.FacebookModel in val.__bases__]
        test_models.insert(0, test_models.pop(test_models.index(models.AdAccount)))
        self.test_models = test_models
        self.test_model_ids = {models.AdAccount: ['act_' + str(self.account_id)]}
        if self.test_live_endpoints and not hasattr(self, 'pyfb'):
            self.pyfb = PyFacebook(app_id=self.app_id, app_secret=self.app_secret, token_text=self.test_token_text)

    def tearDown(self):
        self.shelf.close()

    def __handle_results(self, results):
        """
        Validates a resultset, and appends valid models to test_model_ids.

        :param dict results: A resultset from PyFacebook.get

        """
        first_model = first_item(results['data'])
        if first_model and hasattr(first_model, 'id'):
            first_model.validate()
            self.test_model_ids[type(first_model)] = [str(first_model.id)]

    def __test_get_single_endpoint(self, test_model, test_id, connection=None, parent_model=None):
        """
        Tests a single Facebook Ads endpoint

        :param FacebookModel test_model: The model returned by this endpoint
        :param str connection: The name of the connection, if we are testing one.
        :param FacebookModel parent_model: The parent model of the connection, if we are testing one.

        """
        print "\n\n================"
        if connection:
            print "TEST GET FOR CONNECTION", parent_model.__name__, connection, "WITH ID", test_id
            if self.test_live_endpoints:
                results = self.pyfb.get(test_model, id=test_id, connection=connection, return_json=True, limit=self.limit_live_results)
                self.shelf[str(test_id) + "__" + connection + "__GET__"] = results
                print "GOT RESULTS:"
                pprint(results)
                results['data'] = json_to_objects(results['data'], test_model)
            else:
                results = self.shelf[str(test_id) + "__" + connection + "__GET__"]
                results['data'] = json_to_objects(results['data'], test_model)
        else:
            print "TEST GET FOR", test_model.__name__, "WITH ID", test_id
            if self.test_live_endpoints:
                results = self.pyfb.get(test_model, id=test_id, return_json=True, limit=self.limit_live_results)
                self.shelf[str(test_id) + "__GET__"] = results
                results['data'] = json_to_objects(results['data'], test_model)
            else:
                results = self.shelf[str(test_id) + "__GET__"]
                results['data'] = json_to_objects(results['data'], test_model)
        print "GOT RESULTS"
        pprint(results)
        self.__handle_results(results)

    def test_exchange_access_token(self):
        """
        Test for the fb_exchange_token functionality of the /oauth/access_token endpoint

        """
        if self.test_live_endpoints:
            self.pyfb = PyFacebook(app_id=self.app_id, app_secret=self.app_secret, token_text=self.test_token_text)
            new_token = self.pyfb.exchange_access_token(current_token=self.pyfb.access_token, app_id=self.app_id, app_secret=self.app_secret)

    def test_get(self):
        """
        Test for the GET functionality of all defined FacebookModels and their connections.
        AdAccount is tested first, using FACEBOOK_TEST_ACCOUNT_ID as the id.
        Connected models are then tested, using the ids from previous results.

        """
        for test_model in self.test_models:
            if test_model not in self.test_model_ids.keys():
                print "\n\n==== SKIPPING TEST! NO TEST ID FOR", test_model.__name__, "===="
            else:
                for test_id in self.test_model_ids[test_model]:
                    self.__test_get_single_endpoint(test_model=test_model, test_id=test_id)
                    for connection in getattr(test_model, 'CONNECTIONS', []):
                        connection_field_def = next(f for f in test_model.FIELD_DEFS if f.title == connection)
                        child_model = first_item(connection_field_def.allowed_types[0])
                        self.__test_get_single_endpoint(test_model=child_model, test_id=test_id, connection=connection, parent_model=test_model)
