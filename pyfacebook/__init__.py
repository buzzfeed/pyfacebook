import json
import time
import requests
import datetime
import warnings

from urlparse import parse_qs
from pyfacebook import models
from pyfacebook.fault import FacebookException
from tinymodel.service import Service

from pyfacebook.settings import(
    USE_LONG_LIVED_TOKENS,
)


class PyFacebook(object):

    """
    The Facebook class's methods will return an object reflecting the Facebook Graph API

    """
    __graph_url = "https://graph.facebook.com"
    #__service = Service(return_type='tinymodel', find=get)


    def __init__(self, app_id=None, app_secret=None, token_text=None, account_id=None):
        """
        Initializes an object of the Facebook class. Sets local vars and establishes a connection.

        :param long app_id: Facebook app_id

        :param string app_secret: Facebook app_secret

        :param string access_token: Facebook access_token

        :param boolean raw_data: Reserved for future use

        """

        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = self.validate_access_token(token_text=token_text)
        self.account_id = account_id

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
        token_dict = debug_response['data'][0]
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
        :param models.Token token: A Token object representing the current access_token.
        :param str app_id: A Facebook app_id.
        :param str app_secret: A Facebook app_secret.

        :rtype models.Token: New Facebook token
        """
        facebook_token_url = self.__graph_endpoint + '/oauth/access_token'
        if not(current_token and app_id and app_secret):
            raise Exception("Must set app_id, app_secret and access_token before calling exchange_token")

        auth_exchange_params = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": current_token.text,
        }

        resp = requests.get(self.__graph_url + "/oauth/access_token", params=auth_exchange_params)
        new_token_text = parse_qs(resp.text)['access_token'][0]
        return self.__call_token_debug(token_text=new_token_text, input_token_text=new_token_text)


    def call_graph_api(self, endpoint, url=__graph_url, params={}):
        """
        This method calls the Facebook graph api, given an endpoint and a set of params.

        :param str endpoint: The endpoint to call.
        :param str url: The URL to call. This defaults to the standard graph API url.
        :param dict params: A dict of params to attach to the graph API call.

        :rtype dict: A dict representing the json-decoded result from Facebook.
        """
        #Append access_token if not sent in params
        if not params.get('access_token') and self.__access_token:
            params['access_token'] = self.__access_token

        #Pop account_id and append to url if it exists in params
        if params.get('account_id'):
            account_id = params.pop('account_id')
            if type(account_id) in (str, unicode) and 'act_' in account_id:
                url += ('/' + account_id)
            else:
                url += ('/act_' + str(account_id))

        #Get response and standardize for edge cases, raising Facebook errors if they exist
        response = requests.get(url + '/' + endpoint, params=params)
        json_response = response.json()
        if json_response.get('error'):
            raise FacebookException(message=json_response['error']['message'], code=json_response['error']['code'])
        elif json_response.get('data') and json_response['data'].get('error'):
            raise FacebookException(message=json_response['data']['error']['message'], code=json_response['data']['error']['code'])
        elif not json_response.get('data'):
            json_response = {'data': [json_response]}
        elif not isinstance(json_response['data'], list):
            json_response['data'] = [json_response['data']]

        return json_response

    def get(self, model, limit=None, offset=None, **kwargs):
        """
        Sends an Ads API call to Facebook and retrieves a JSON response
        Search params are sent as keyword args.

        :rtype dict: A dict with results. Typical keys are data, errors and paging.
                     Data is always a list of TinyModels.
        """
        pass

