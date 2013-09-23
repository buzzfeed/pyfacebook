import json
import time
import requests
import datetime
import warnings

from urlparse import parse_qs
from pyfacebook import models
from pyfacebook.fault import FacebookException
from pyfacebook.utils import json_to_objects

from pyfacebook.settings import(
    USE_LONG_LIVED_TOKENS,
    FACEBOOK_GRAPH_URL,
)


class PyFacebook(object):

    """
    The Facebook class's methods will return an object reflecting the Facebook Graph API

    """

    def __init__(self, app_id=None, app_secret=None, token_text=None):
        """
        Initializes an object of the Facebook class. Sets local vars and establishes a connection.

        :param str app_id: Facebook app_id
        :param str app_secret: Facebook app_secret
        :param str token_text: Facebook access_token

        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = self.validate_access_token(token_text=token_text)

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

    def validate_access_token(self, token_text, input_token_text=None, use_long_lived_tokens=USE_LONG_LIVED_TOKENS):
        """
        Calls the Facebook token debug endpoint, to validate the access token and provide token info.

        :param str token_text: The oauth token used to access your Facebook app
        :param str input_token_text: The token you wish to validate. This will default to token_text if not provided.
        :param bool use_long_lived_tokens: A flag to indicate whether you wish to use long-lived tokens.
                                           If True, this will automatically exchange any tokens
                                           about to expire in 24 hours and raise a warning.
        :rtype models.Token: A model representing the access_token

        """
        if not input_token_text:
            input_token_text = token_text

        my_token = self.__call_token_debug(token_text, input_token_text)

        if USE_LONG_LIVED_TOKENS and (my_token.expires_at - datetime.datetime.utcnow()).days < 1:
            my_new_token = self.exchange_access_token(current_token=my_token, app_id=self.app_id, app_secret=self.app_secret)
            warnings.warn("""WARNING: Your current Facebook API token is about to expire.
                           Replace your stored token with this new one: """ + "\n" + my_new_token.text)
            return my_new_token
        else:
            return my_token

    def exchange_access_token(self, current_token, app_id, app_secret):
        """
        Exchange an existing token for a new long-term token.
        :param models.Token current_token: A Token object representing the current access_token.
        :param str app_id: A Facebook app_id.
        :param str app_secret: A Facebook app_secret.

        :rtype models.Token: New Facebook token
        """
        # Response is not even JSON so it requires a custom call to the graph api
        facebook_token_url = FACEBOOK_GRAPH_URL + '/oauth/access_token'
        if not(current_token and app_id and app_secret):
            raise Exception("Must set app_id, app_secret and access_token before calling exchange_token")

        auth_exchange_params = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": current_token.text,
        }

        resp = requests.get(FACEBOOK_GRAPH_URL + "/oauth/access_token", params=auth_exchange_params)
        try:
            json_response = resp.json()
            if json_response.get('error'):
                raise FacebookException(message=json_response['error']['message'], code=json_response['error']['code'])
        except ValueError:
            pass
        new_token_text = parse_qs(resp.text)['access_token'][0]
        return self.__call_token_debug(token_text=new_token_text, input_token_text=new_token_text)

    def call_graph_api(self, endpoint, url=FACEBOOK_GRAPH_URL, params={}):
        """
        This method calls the Facebook graph api, given an endpoint and a set of params.

        :param str endpoint: The endpoint to call.
        :param str url: The URL to call. This defaults to the standard graph API url.
        :param dict params: A dict of params to attach to the graph API call.

        :rtype dict: A dict representing the json-decoded result from Facebook.

        """
        # Append access_token if not sent in params
        if not params.get('access_token') and self.access_token.text:
            params['access_token'] = self.access_token.text

        # Get response and standardize for edge cases, raising Facebook errors if they exist
        response = requests.get(url + '/' + endpoint, params=params)
        json_response = response.json()
        if json_response.get('error'):
            raise FacebookException(message=json_response['error']['message'], code=json_response['error']['code'])
        elif not json_response.get('data'):
            json_response = {'data': [json_response]}
        return json_response

    def get(self, model, id=None, connection=None, limit=None, offset=None, return_json=False):
        """
        Sends an Ads API call to Facebook and retrieves a JSON response
        Search params are sent as keyword args.

        :param tinymodel.TinyModel model: The class associated with the objects we're getting.
        :param str connection: The name of the connection, if we're getting connected objects.
        :param int limit: A limit on the number of objects returned.
        :param int offset: The offset of the objects returned, as defined by Facebook.
        :param bool return_json: Should return a json string

        :rtype dict: A dict with results. Typical keys are data, errors and paging.
                     Data is always an iterable of TinyModels.
        """
        params = {key: val for key, val in {'limit': limit,
                                            'offset': offset,
                                            }.items() if val}
        if id:
            endpoint = str(id)
        else:
            endpoint = model.__name__.lower()

        if connection:
            endpoint += ('/' + connection)

        fb_response = self.call_graph_api(endpoint=endpoint, params=params)
        if not return_json:
            fb_response['data'] = json_to_objects(fb_response['data'], model)

        return fb_response
