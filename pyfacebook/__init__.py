import json
import pytz
import requests
import datetime
import warnings
import inflection

from urlparse import parse_qs
from pyfacebook import models
from simplejson.decoder import JSONDecodeError
from pprint import pprint

from pyfacebook.utils import(
    FacebookException,
    json_to_objects,
)


class PyFacebook(object):

    """
    The Facebook class's methods will return an object reflecting the Facebook Graph API

    """

    def __init__(self, app_id=None, app_secret=None, token_text=None,
                 use_long_lived_tokens=True, call_token_debug=True,
                 facebook_graph_url='https://graph.facebook.com'):
        """
        Initializes an object of the Facebook class. Sets local vars and establishes a connection.

        :param str app_id: Facebook app_id
        :param str app_secret: Facebook app_secret
        :param str token_text: Facebook access_token
        :param bool call_token_debug: wether to validate or not the token_text.

        """
        self.__use_long_lived_tokens = use_long_lived_tokens
        self.__facebook_graph_url = facebook_graph_url

        self.app_id = app_id
        self.app_secret = app_secret
        self.call_token_debug = call_token_debug
        if self.call_token_debug:
            self.access_token = self.validate_access_token(token_text=token_text)
        else:
            self.access_token = models.Token(text=token_text)

    def __call_token_debug(self, token_text, input_token_text):
        """
        Calls the Facebook debug_token endpoint and returns a Token object.

        :param str token_text: The oauth token used to access your Facebook app
        :param str input_token_text: The token you wish to validate.

        :rtype models.Token:

        """
        token_debug_params = {'access_token': token_text,
                              'input_token': input_token_text}
        debug_response = self.call_graph_api(endpoint='debug_token', params=token_debug_params)
        token_dict = debug_response['data']
        if token_dict.get('error'):
            raise FacebookException(message=token_dict['error']['message'], code=token_dict['error']['code'])
        token_dict['text'] = input_token_text
        return models.Token(from_json=json.dumps(token_dict))

    def __call_endpoint(self, model, id, connection, http_method, params, return_json):
        """
        Creates a properly-formatted Facebook Graph API endpoint from id and connection parameters.
        Performs an endpoint call and returns the result.

        :param tinymodel.TinyModel model: The class associated with the objects we're getting.
        :param str id: The id of the parent object
        :param str connection: The name of connection to call
        :param str http_method: The type of call to make
        :param dict params: The params to send in the call
        :param bool return_json: If True, the call returns a dict instead of TinyModel objects

        """
        endpoint = str(id or model.endpoint or model.__name__.lower())

        if connection:
            endpoint += ('/' + connection)

        fb_response = self.call_graph_api(endpoint=endpoint, http_method=http_method, params=params)
        if not return_json:
            fb_response['data'] = json_to_objects(fb_response['data'], model)

        return fb_response

    def __convert_datetime_to_facebook(self, field_name, this_datetime):
        """
        Converts any date or datetime to the proper format for a Facebook call

        Facebook expects UTC times so if we get anything other than UTC than we raise a warning and convert if possible

        :param str field_name: The name of the field we're converting
        :param datetime this_datetime: The datetime we want to convert
        :rtype str: A string representing the Facebook time

        """
        if not isinstance(this_datetime, datetime.datetime):
            if not isinstance(this_datetime, datetime.date):
                raise Exception(field_name + " needs to be either a date or a datetime object")
            else:
                this_datetime = datetime.datetime(this_datetime.year, this_datetime.month, this_datetime.day)

        if not this_datetime.tzinfo:
            warnings.warn("WARNING: Your parameter " + field_name + " was sent as a naive datetime.\n"
                          "Facebook expects UTC datetimes only, so we are sending as UTC.\n"
                          "Please send timezone-aware datetimes in the future.")
        elif not this_datetime.tzinfo == pytz.utc:
            warnings.warn("WARNING: Your parameter " + field_name + " was not sent as UTC.\n"
                          "Facebook expects UTC datetimes only, so we are converting it to UTC.\n"
                          "Please send UTC datetimes in the future.")
            this_datetime = this_datetime.astimezone(pytz.utc)

        return this_datetime.replace(tzinfo=None, minute=0, second=0, microsecond=0).isoformat()

    def __delete_everything(self, account_id):
        """
        Utility function for testing purposes. Deletes all adgroups, adcampaigns and adcreatives in the passed-in account.
        This is obviously an extremely destructive method so USE CAUTION!!!

        """
        adgroups = self.get(model=models.AdGroup, id=account_id, connection='adgroups')['data']
        for adgroup in adgroups:
            self.delete(id=adgroup.id)
        print "DELETED", len(adgroups), "ADGROUPS"

        adcreatives = self.get(model=models.AdCreative, id=account_id, connection='adcreatives')['data']
        for adcreative in adcreatives:
            self.delete(id=adcreative.id)
        print "DELETED", len(adcreatives), "ADCREATIVES"

        adcampaigns = self.get(model=models.AdSet, id=account_id, connection='adcampaigns')['data']
        for adcampaign in adcampaigns:
            self.delete(id=adcampaign.id)
        print "DELETED", len(adcampaigns), "ADCAMPAIGNS"

    def validate_access_token(self, token_text, input_token_text=None):
        """
        Calls the Facebook token debug endpoint, to validate the access token and provide token info.

        :param str token_text: The oauth token used to access your Facebook app
        :param str input_token_text: The token you wish to validate. This will default to token_text if not provided.
        :rtype models.Token: A model representing the access_token

        """
        if not input_token_text:
            input_token_text = token_text
        my_token = self.__call_token_debug(token_text, input_token_text)

        token_expires_soon = my_token.expires_at and \
            my_token.expires_at > datetime.datetime(1970, 1, 1, 0, 0) and \
            (my_token.expires_at - datetime.datetime.utcnow()).days < 1
        if self.__use_long_lived_tokens and token_expires_soon:
            my_new_token = self.exchange_access_token(current_token=my_token, app_id=self.app_id, app_secret=self.app_secret)
            warnings.warn("WARNING: Your current Facebook API token is about to expire.\n"
                          "Replace your stored token with this new one:\n" + my_new_token.text)
            return my_new_token
        else:
            return my_token

    def exchange_access_token(self, current_token=None, app_id='', app_secret=''):
        """
        Exchange an existing token for a new long-term token.
        :param models.Token current_token: A Token object representing the current access_token.
        :param str app_id: A Facebook app_id.
        :param str app_secret: A Facebook app_secret.

        :rtype models.Token: New Facebook token

        """
        auth_exchange_params = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": current_token.text,
        }
        resp = self.call_graph_api('oauth/access_token', expect_json=False, params=auth_exchange_params)
        new_token_text = parse_qs(resp)['access_token'][0]
        if self.call_token_debug:
            return self.__call_token_debug(token_text=new_token_text, input_token_text=new_token_text)
        else:
            return new_token_text

    def call_graph_api(self, endpoint, http_method='GET', expect_json=True, params={}):
        """
        This method calls the Facebook graph api, given an endpoint and a set of params.

        :param str endpoint: The endpoint to call.
        :param str http_method: The http method to use. Currently supports only GET, POST and DELETE
        :param dict params: A dict of params to attach to the graph API call.

        :rtype dict: A dict representing the json-decoded result from Facebook.

        """
        # Append access_token if not sent in params
        if not (params.get('access_token') or params.get('fb_exchange_token')) and hasattr(self, 'access_token'):
            params['access_token'] = self.access_token.text

        # Dump iterable params to JSON if possible
        for key, val in params.items():
            if isinstance(val, (list, dict, tuple, set)):
                try:
                    params[key] = json.dumps(val)
                except (TypeError, ValueError):
                    pass
            elif isinstance(val, (datetime.date, datetime.datetime)):
                params[key] = self.__convert_datetime_to_facebook(key, val)

        # MAKE THE CALL
        url = self.__facebook_graph_url
        if http_method == 'GET':
            response = requests.get(url + '/' + endpoint, params=params)
        elif http_method == 'POST':
            post_file = params.pop('file', None)
            if post_file:
                response = requests.post(url + '/' + endpoint, files=post_file, data=params)
            else:
                response = requests.post(url + '/' + endpoint, data=params)
        elif http_method == 'DELETE':
            response = requests.delete(url + '/' + endpoint, params=params)
        else:
            raise Exception("Called Facebook Graph API with unsupported method: " + http_method)

        # Parse response and standardize for edge cases, raising Facebook errors if they exist
        try:
            json_response = response.json()
            if not isinstance(json_response, dict):
                raise ValueError
            elif json_response.get('error'):
                raise FacebookException(message=json_response['error']['message'], code=json_response['error']['code'])
            elif json_response.get('images'):
                json_response = {'data': json_response['images']}
            elif not json_response.get('data'):
                json_response = {'data': [json_response]}
            return json_response
        except ValueError, JSONDecodeError:
            if expect_json:
                print "ERROR CALLING FB URL: %s" % (url + '/' + endpoint)
                print "WITH PARAMS:"
                pprint(params)
                raise Exception('Expected Valid JSON response, got this instead: %s' % response.text)
            return response.text

    def get(self, model, id, connection=None, return_json=False, **kwargs):
        """
        Sends an Ads API GET call to Facebook and retrieves a JSON response

        :param tinymodel.TinyModel model: The class associated with the objects we're getting.
        :param str id: The Facebook id of the object we're getting.
        :param str connection: The name of the connection, if we're getting connected objects.
        :param bool return_json: Should return a json string

        :rtype dict: A dict with results. Typical keys are data, errors and paging.
                     If return_json is False, data is an iterable of TinyModels.

        """
        if not id:
            raise Exception("Need an ID in order to make a GET request to the Facebook API.")

        params = {}
        if not kwargs.get('fields'):
            fields_to_get = [f.title for f in model.FIELD_DEFS
                             if f.title not in getattr(model, 'CONNECTIONS', []) and
                             f.title not in getattr(model, 'CREATE_ONLY', [])]
            params = {'fields': fields_to_get}

        params.update(kwargs)
        return self.__call_endpoint(model=model, id=id, connection=connection, http_method='GET', params=params, return_json=return_json)

    def post(self, model, id=None, connection=None, return_json=False, **kwargs):
        """
        Sends an Ads API POST call to Facebook and retrieves a JSON response
        POST params are recevied as keyword args.

        :param tinymodel.TinyModel model: The class associated with the object we're POSTing.
        :param bool return_json: Should return a json string

        :rtype dict: A dict with the POST response. JSON models are translated to TinyModels where appropriate.

        """
        if not connection:
            connection = inflection.pluralize(model.__name__.lower())
        return self.__call_endpoint(model=model, id=id, connection=connection, http_method='POST', params=kwargs, return_json=return_json)

    def delete(self, id, **kwargs):
        """
        Sends an Ads API DELETE call to Facebook and retrieves a JSON response
        POST params are recevied as keyword args.

        :param str id: The Facebook id of the parent object if we need to specify one

        :rtype bool: A flag indicating whether the object was deleted successfully.

        """
        resp = self.call_graph_api(endpoint=str(id), http_method='DELETE', expect_json=False)
        if resp != 'true':
            warnings.warn("WARNING: DELETE called on Facebook object with id " + str(id) + ""
                          "But the object may not have been deleted. Facebook says:\n" + resp)
            return False
        else:
            return True
