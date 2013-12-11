import unittest
import anydbm
import inflection

from caliendo.patch import patch
from nose.tools import ok_
from pyfacebook import(
    settings,
    models,
    PyFacebook,
)

import post_fixtures
import get_fixtures

from pyfacebook.utils import(
    first_item,
    json_to_objects,
)

anydbm._defaultmod = __import__('dumbdbm')


class FacebookModelsTest(unittest.TestCase):
    """ Tests PyFacebook functionality for all Facebook models. """

    limit_live_results = settings.__dict__.get('LIVE_TEST_RESULTSET_LIMIT')

    app_id = settings.__dict__.get('FACEBOOK_TEST_APP_ID')
    app_secret = settings.__dict__.get('FACEBOOK_TEST_APP_SECRET')
    test_token_text = settings.__dict__.get('FACEBOOK_TEST_ACCESS_TOKEN')
    account_id = settings.__dict__.get('FACEBOOK_TEST_ACCOUNT_ID')
    if account_id:
        account_id = account_id if account_id[0:4] == 'act_' else 'act_' + account_id

    def set_up_get_model_ids(self):
        return {models.AdAccount.__name__: [self.account_id]}

    @patch('test.models_test.FacebookModelsTest.set_up_get_model_ids')
    def setUp(self):
        """ Set up models list and PyFacebook instance """

        get_models = [val for key, val in models.__dict__.items() if isinstance(val, type) and models.FacebookModel in val.__bases__]
        get_models.insert(0, get_models.pop(get_models.index(models.AdAccount)))
        self.get_models = get_models
        self.get_model_ids = self.set_up_get_model_ids()

    def _test_exchange_access_token(self):
        pyfb = PyFacebook(app_id=self.app_id, app_secret=self.app_secret, token_text=self.test_token_text)
        pyfb.exchange_access_token(current_token=pyfb.access_token, app_id=self.app_id, app_secret=self.app_secret)

    @patch('test.models_test.FacebookModelsTest._test_exchange_access_token')
    def test_exchange_access_token(self):
        """
        Test for the fb_exchange_token functionality of the /oauth/access_token endpoint

        """
        self._test_exchange_access_token()

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

    def _test_single_endpoint(self, model, http_method, id=None, connection=None, return_json=True, **kwargs):
        """
        Tests a single Facebook Ads endpoint

        :param FacebookModel model: The model returned by this endpoint
        :param str connection: The name of the connection, if we are testing one.

        """
        model_name = None
        this_model_ids = []
        pyfb = PyFacebook(app_id=self.app_id, app_secret=self.app_secret, token_text=self.test_token_text)
        test_method = getattr(pyfb, http_method.lower())
        results = test_method(model=model, id=id, connection=connection, return_json=return_json, **kwargs)

        if return_json:
            results['data'] = json_to_objects(results['data'], model)
            first_obj = first_item(results['data'])
            if first_obj and hasattr(first_obj, 'id'):
                first_obj.validate()
                model_name = type(first_obj).__name__
                this_model_ids = [first_obj.id]
            results = first_obj
        if hasattr(results, 'to_json'):
            results = results.to_json(return_dict=True)
        return results, (model_name, this_model_ids)

    def _run_post_call(self, model, connection, **params):
        return self._test_single_endpoint(model=model, http_method='POST', id=self.account_id, connection=connection, **params)

    @patch('test.models_test.FacebookModelsTest._test_single_endpoint')
    @patch('test.models_test.FacebookModelsTest._run_post_call')
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
            model = post_dict['model']
            for fixture_name, fixture_obj in post_fixtures.FIXTURES[model].items():
                # set ids or hashes of dependent objects if appropriate
                self.__add_dependent_ids(post_dict.get('dependent_fields', {}), fixture_obj)
                if hasattr(fixture_obj, 'file'):
                    post_params = dict([(f.field_def.title, f.value) for f in fixture_obj.FIELDS])
                else:
                    post_params = fixture_obj.to_json(return_dict=True)

                post_params.pop('id', None)
                post_params.pop('hash', None)
                connection = inflection.pluralize(model.__name__.lower())
                return_obj, (model_name, model_ids) = self._run_post_call(model, connection, **post_params)
                if model_name and model_ids:
                    self.get_model_ids[model_name] = model_ids
                if 'id' in return_obj:
                    fixture_obj.id = return_obj['id']
                elif 'hash' in return_obj:
                    fixture_obj.hash = return_obj['hash']

        # test GET using fixtures
        for model in self.get_models:
            if model.__name__ not in self.get_model_ids.keys():
                print "==== SKIPPING GET TEST! NO TEST ID FOR", model.__name__, "===="
                continue
            for id in self.get_model_ids[model.__name__]:
                self._test_single_endpoint(model=model, http_method='GET', id=id, limit=self.limit_live_results)
                for connection in getattr(model, 'CONNECTIONS', []):
                    connection_field_def = next(f for f in model.FIELD_DEFS if f.title == connection)
                    child_model = first_item(connection_field_def.allowed_types[0])
                    extra_params = get_fixtures.CONNECTIONS.get(model, {}).get(connection, {})
                    self._test_single_endpoint(model=child_model, http_method='GET', id=id, connection=connection, limit=self.limit_live_results, **extra_params)

        # test DELETE by deleting posted models from above
        post_fixtures.POST_MODELS.reverse()
        for post_dict in post_fixtures.POST_MODELS:
            model = post_dict['model']
            for fixture_name, fixture_obj in post_fixtures.FIXTURES[model].items():
                if hasattr(fixture_obj, 'id'):
                    ok_(self._test_single_endpoint(model=model, id=fixture_obj.id, http_method='DELETE', return_json=False)[0])
