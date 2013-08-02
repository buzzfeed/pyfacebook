from pyfacebook.api import Model, FieldDef
from pyfacebook.fault import FacebookException


class BroadTargetingCategory(Model):
    """
    The BroadTargetingCategory class represents the broadtargetingcategory object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/
    We extend the functionality in the documentation with custom calls for adaccounts
    """
    FIELD_DEFS = [
        FieldDef(title='id', required=False, allowed_types=[int]),
        FieldDef(title='name', required=False, allowed_types=[str]),
        FieldDef(title='parent_category', required=False, allowed_types=[str]),
        FieldDef(title='size', required=False, allowed_types=[int]),
    ]

    def find_by_adaccount_id(self, adaccount_id):
        """
        Retrieves BroadTargetingCategory objects associated with this AdAccount

        :param int adaccount_id: The adaccount id

        :rtype: List of BroadTargetingCategory objects contained by this AdAccount
        """
        if not adaccount_id:
            raise FacebookException("Must set an id before making this call")
        btcs = self._fb.get_all('/act_' + str(adaccount_id) + '/broadtargetingcategories')
        return [self.from_json(btc, preprocessed=True) for btc in btcs]
