from pyfacebook.models import Model


class BroadTargetingCategory(Model):

    """
    The BroadTargetingCategory class represents the broadtargetingcategory object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/broadtargetingcategory/
    We extend the functionality in the documentation with custom calls for adaccounts

    """

    attrs_to_copy = ('id', 'name', 'parent_category', 'size')
