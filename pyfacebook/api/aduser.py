import json as j
from pyfacebook.api import Model
from tinymodel import FieldDef
from pyfacebook.fault import FacebookException


class AdUser(Model):
    """
    The AdUser class represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/aduser/
    We extend the functionality in the documentation with custom calls for adaccounts
    """
    FIELD_DEFS = [
        FieldDef(title='id', required=False, allowed_types=[long]),
        FieldDef(title='role', required=False, allowed_types=[int]),
    ]

    def find_by_adaccount_id(self, adaccount_id):
        """
        Retrieves User objects associated with this AdAccount

        :param int adaccount_id: The adaccount id

        :rtype: List of AdUsers contained by this AdAccount
        """
        if not adaccount_id:
            raise FacebookException("Must set an id before making this call")
        users = self._fb.get_all('/act_' + str(adaccount_id) + '/users')

        return [self.__class__(from_json=j.dumps(aduser)) for aduser in users]
