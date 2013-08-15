import urllib
import urllib2
import json
import time
from urlparse import parse_qs
from urlparse import urlparse
from pyfacebook.fault import FacebookException
from caliendo.facade import cache as caliendo_cache


class PyFacebook(object):

    """
    The Facebook class's methods will return an object reflecting the Facebook Graph API

    """
    __app_id = None
    __app_secret = None
    __access_token = None
    __graph_endpoint = "https://graph.facebook.com"

    def __init__(self, app_id, access_token=None, app_secret=None, raw_data=False):
        """
        Initializes an object of the Facebook class. Sets local vars and establishes a connection.

        :param long app_id: Facebook app_id

        :param string app_secret: Facebook app_secret

        :param string access_token: Facebook access_token

        :param boolean raw_data: Reserved for future use

        """

        self.__app_id = app_id
        self.__app_secret = app_secret
        self.__access_token = access_token

    def get_list_from_fb(self, container_obj_id, converter, params={}, fields=[]):
        """
        Retrieves data from Facebook and returns it as a list of objects.

        :param string container_obj_id: The id of the container object.
        :param ValidatedModel converter: The object to translate dict to.
        :param dict params: A dictionary containing lookup parameters.
        :param list fields: A list of fields to be retrieved in request.

        :rtype: List of objects of Class converter, representing data pulled from the Facebook Graph API

        """
        resource = '/' + str(container_obj_id) + '/' + converter.__class__.__name__.lower() + 's'
        objs = self.get_all(resource, params, fields=fields)
        return [converter.__class__().from_json(self.preprocess_json(obj), preprocessed=True) for obj in objs]

    def get_many_from_fb(self, obj_ids, converter, fields=[]):
        """
        Retrieves data form Facebook and returns a list of models representing the pulled resources.

        :param list(<int>) obj_ids: A list of ids for the objects to pull from FB
        :param ValidatedModel converter: The object to translate dict to.
        :param list fields: A list of fields to be retrieved in request.

        :rtype <list<model>:
        """
        if not obj_ids:
            raise FacebookException("A list of ids is required")
        objs = []
        base_url = ''
        params = {}
        params["ids"] = ",".join(map(str, obj_ids))

        resp = self.get(base_url, params, fields=fields)
        objs += resp.values()
        return [converter.__class__().from_json(self.preprocess_json(obj), preprocessed=True) for obj in objs]

    def get_one_from_fb(self, reference_obj_id, converter, fields=[]):
        """
        Retrieves data from Facebook and returns it as an object.

        :param string reference_obj_id: The id of the reference object.
        :param ValidatedModel converter: The object to translate dict to.
        :param list fields: A list of fields to be retrieved in request.

        :rtype: Object of Class converter, representing data pulled from the Facebook Graph API

        """
        resp = self.get('/' + str(reference_obj_id))
        return converter.__class__().from_json(self.preprocess_json(resp), preprocessed=True)

    def create(self, converter, **kwargs):
        """
        Creates a new instance on type <model> with the given <kwargs>

        :param ValidatedModel converter: The handle of the model we're creating

        :rtype A dict with the attributes of the remote obj, the new model instance with the given attribute.
        """
        try:
            account_id = kwargs.pop('account_id')
        except KeyError:
            raise FacebookException('An account_id is required to make the request!')

        url = '/act_{account_id}/{model}s'.format(account_id=account_id, model=converter.__class__.__name__.lower())
        response = self.post(url, urllib.urlencode(kwargs))
        return converter.__class__.from_json(self.preprocess_json(response), preprocessed=True)

    def update(self, obj_id, **kwargs):
        """
        Sends an update request for obj_id with the given kwargs.

        :rtype dict The data retrieved by the request after updating.
        """
        url = '/{obj_id}'.format(obj_id=obj_id)
        response = self.post(url, urllib.urlencode(kwargs))
        return response

    def clean_params(self, clean_empty_strings=True, **kwargs):
        """
        Remove null and falsy values from an argument list.
        """
        cleaned_data = dict()
        for k, v in kwargs.iteritems():
            if not v:
                if isinstance(v, str) and not clean_empty_strings:
                    cleaned_data[k] = v
            else:
                cleaned_data[k] = v
        return kwargs

    def get_all(self, resource, params={}, fields=[]):
        """
        Return all the results requested as implied by the params sent regardless of FB's limitations.

        :param str resource: The URI for the resource on the Facebook graph endpoint
        :param dict params: The additional parameters for the request. These can include but are not limited to limit and offset.
        :param list fields: A list of fields to be retrieved in request.

        :rtype list(<mixed>): The return objects
        """
        data = []
        limit = int(params.get('limit', 0))
        offset = int(params.get('offset', 0))
        resp = {}
        while True:
            resp = self.get(resource, params, fields=fields)
            data += resp['data']
            if limit and not offset:
                return data[0:limit]
            if limit and offset:
                return data[offset:offset + limit]
            if not limit and offset:
                return data[offset:]
            if 'paging' in resp and 'next' in resp['paging']:
                next_url = resp['paging']['next']
                url = urlparse(next_url)
                resource = url.path
                params = dict([(key, val[0]) for key, val in parse_qs(url.query).items()])
            else:
                break
        return data

    def _json_response(self, url, data=None):
        response = urllib.urlopen(url, data)
        raw_response = response.read()
        resp = json.loads(raw_response)
        response.close()
        return resp

    def get(self, resource, params={}, fields=[]):
        """
        GET's a FB response for a given resource and set of parameters. Automatically passes the access_token.

        :rtype dict: The JSON response.
        """
        url = self.__graph_endpoint + str(resource)
        if '?' in url:
            url += '&'
        else:
            url += '?'
        url += 'access_token=' + str(self.__access_token)

        if fields:
            url += '{}{}'.format('&fields=', ','.join(fields))

        if params:
            url += '&'
            url += urllib.urlencode(params)

        resp = caliendo_cache(handle=self._json_response, kwargs={'url': url})

        if 'error' in resp:
            time.sleep(5)
            resp = caliendo_cache(handle=self._json_response, kwargs={'url': url})
            if 'error' in resp:
                raise FacebookException(resp['error'])

        return resp

    def post(self, resource, payload):
        """
        Issues an HTTP POST request to the resource with params as the payload
        """
        url = '{base_url}{source_url}'.format(base_url=self.__graph_endpoint, source_url=str(resource))
        url += '&' if '?' in url else '?'
        url += urllib.urlencode({'access_token': self.access_token()})
        obj = caliendo_cache(handle=self._json_response, kwargs={'url': url, 'data': payload})

        try:
            if 'error' in obj:
                raise FacebookException(obj['error'])
        except TypeError:  # update calls simply return True, so it's not iterable, but correct
            pass

        return obj

    def delete(self, resource, params, content_type='application/json'):
        """
        Issues an HTTP DELETE request to the resource with params as the payload
        """
        url = self.__graph_endpoint + str(resource)
        opener = urllib2.build_opener(urllib2.HTTPSHandler)
        request = urllib2.Request(url, data=params)
        request.add_header('Content-Type', content_type)
        request.get_method = lambda: 'DELETE'
        response = opener.open(request)
        raw_response = response.read()
        response.close()
        return raw_response

    def access_token(self, access_token=None):
        if access_token:
            self.__access_token = access_token
        return self.__access_token

    def exchange_token(self):
        """
        Exchange an existing token for a new one. Token should be set ( and valid! ) before you call this.

        :rtype: New Facebook token
        """
        facebook_token_url = self.__graph_endpoint + '/oauth/access_token'
        if self.__app_id is None or self.__app_secret is None or self.__access_token is None:
            raise FacebookException("Must set app_id, app_secret and access_token before calling exchange_token")

        auth_exchange_params = {
            "client_id": self.__app_id,
            "client_secret": self.__app_secret,
            "grant_type": "fb_exchange_token",
            "fb_exchange_token": self.__access_token
        }

        auth_exchange_url = "%s%s%s" % (facebook_token_url, "?", urllib.urlencode(auth_exchange_params))
        response = self.get(auth_exchange_url)
        new_token = response[0][1]
        self.__access_token = new_token
        return new_token

    def preprocess_json(self, resp):
        """
        Add support for strings like 'Testing "testing"' and makes facebook api friendly for ValidatedModel

        :param dict resp: Dict response to fix.

        :rtype str: The fixed response.
        """
        for key, value in resp.items():
            if not type(value) in [list, dict]:
                if type(value) in [unicode, str]:
                    if key in ['body', 'name', 'title'] and ("'" in value or '"' in value or '\n' in value or '\t' in value):
                        resp[key] = unicode(json.dumps(value))
            if key == 'action_spec' and type(value) not in [type(None)]:
                if type(value) == dict:
                    if value.get('action.type'):
                        if type(value['action.type']) not in [list, type(None)]:
                            value['action.type'] = [value.get('action.type')]
                    resp[key] = [value]
                if type(value) == list:
                    for index, val in enumerate(value):
                        if val.get('action.type'):
                            if type(val['action.type']) not in [list, type(None)]:
                                value[index]['action.type'] = [val.get('action.type')]
        return resp
