from pyfacebook.api import Model, FieldDef
from pyfacebook.fault import FacebookException


class AdGroup(Model):
    """
    The AdGroup class represents an adgroup object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adgroup
    """
    FIELD_DEFS = [
        FieldDef(title='id', required=False, allowed_types=[long]),
        FieldDef(title='campaign_id', required=False, allowed_types=[long]),
        FieldDef(title='name', required=False, allowed_types=[str]),
        FieldDef(title='disapprove_reason_descriptions', required=False, allowed_types=[str]),
        FieldDef(title='adgroup_status', required=False, allowed_types=[int]),
        FieldDef(title='ad_status', required=False, allowed_types=[int]),
        FieldDef(title='bid_info', required=False, allowed_types=[{str: int}, type(None)]),
        FieldDef(title='bid_type', required=False, allowed_types=[int]),
        FieldDef(title='updated_time', required=False, allowed_types=[int, unicode]),
        FieldDef(title='account_id', required=False, allowed_types=[int]),
        FieldDef(title='targeting', required=False, allowed_types=['pyfacebook.api.targeting.Targeting']),
        FieldDef(title='creative_ids', required=False, allowed_types=[[int]]),
    ]

    def find_by_adaccount_id(self, adaccount_id, include_deleted=False, limit=None, offset=None):
        """
        Pulls ALL adgroups for a Facebook ads account

        :param int adaccount_id: The id corresponding to the Facebook account to pull adgroups from.
        :param boolean include_deleted: A flag that determines whether or not to include deleted adgroups in the resultset
        :param int limit: A limit for the number of adcampaign objects to request
        :param int offset: An offset for the adcampaign resultset

        :rtype [ AdGroup ]: A list of the AdGroups found
        """
        if not adaccount_id:
            raise FacebookException("Must pass an adaccount_id to this call")

        if 'act_' not in adaccount_id:
            adaccount_id = 'act_' + adaccount_id

        params = {}
        if include_deleted:
            params["include_deleted"] = "true"
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)

        return self._fb.get_list_from_fb(adaccount_id, self, params)

    def find_by_id(self, adgroup_id):
        """
        Retrieves a single AdGroup object by adgroup ID

        :param int adgroup_id: The id for the adgroup

        :rtype AdGroup: The adgroup corresponding to the id
        """
        if not adgroup_id:
            raise FacebookException("An adgroup_id is required.")
        return self._fb.get_one_from_fb(adgroup_id, self, fields=self.FIELDS_NAME_LIST)

    def find_by_ids(self, adgroup_ids):
        """
        Retreives a list of AdGroup objects from a list of adgroup IDs subject to FB's max values for limit/batch size

        :param list adgroup_ids: The list of adgroup IDs we are searching for

        :rtype [AdGroup]: A tuple of AdGroup objects found.

        """
        return self._fb.get_many_from_fb(adgroup_ids, self, fields=self.FIELDS_NAME_LIST)
