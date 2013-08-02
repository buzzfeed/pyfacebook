from pyfacebook.api import Model, FieldDef
from pyfacebook.fault import FacebookException


class AdAccount(Model):
    """
    The AdAccount class represents the adaccount object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adaccount/
    """
    FIELD_DEFS = [
        FieldDef(title='id', required=False, allowed_types=[str]),
        FieldDef(title='account_id', required=False, allowed_types=[long]),
        FieldDef(title='name', required=False, allowed_types=[unicode]),
        FieldDef(title='account_status', required=False, allowed_types=[int]),
        FieldDef(title='currency', required=False, allowed_types=[str]),
        FieldDef(title='timezone_id', required=False, allowed_types=[int]),
        FieldDef(title='timezone_name', required=False, allowed_types=[str]),
        FieldDef(title='vat_status', required=False, allowed_types=[int]),
        FieldDef(title='daily_spend_limit', required=False, allowed_types=[int]),
        FieldDef(title='amount_spent', required=False, allowed_types=[int]),
        FieldDef(title='adgroups', required=False, allowed_types=['pyfacebook.api.adgroup.AdGroup', type(None)]),
        FieldDef(title='users', required=False, allowed_types=[['pyfacebook.api.aduser.AdUser'], type(None)]),
        FieldDef(title='stats', required=False, allowed_types=['pyfacebook.api.adstatistic.AdStatistic', type(None)]),
        FieldDef(title='broadtargetingcategories', required=False, allowed_types=['pyfacebook.api.broadtargetingcategory.BroadTargetingCategory', type(None)]),
    ]

    def find_by_id(self, adaccount_id):
        """
        Retrieves an AdAccount by the id.

        :param int adaccount_id: The id for the adaccount

        :rtype AdAccount: The AdAccount associated with the id
        """
        if not adaccount_id:
            raise FacebookException("Must pass an adaccount_id")
        return self._fb.get_one_from_fb(adaccount_id, self)
