from pyfacebook.api import Model, FieldDef
from pyfacebook.fault import FacebookException


class AdCampaign(Model):
    """
    The AdCampaign class represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcampaign/
    We extend the functionality in the documentation with custom calls for adcampaigns
    """
    FIELD_DEFS = [
        FieldDef(title='id', required=False, allowed_types=[long]),
        FieldDef(title='account_id', required=False, allowed_types=[long]),
        FieldDef(title='name', required=False, allowed_types=[str]),
        FieldDef(title='start_time', required=False, allowed_types=[int, unicode]),
        FieldDef(title='end_time', required=False, allowed_types=[int, unicode]),
        FieldDef(title='daily_budget', required=False, allowed_types=[int]),
        FieldDef(title='campaign_status', required=False, allowed_types=[int]),
        FieldDef(title='lifetime_budget', required=False, allowed_types=[int]),
    ]

    def find_by_adaccount_id(self, adaccount_id, include_deleted=False, limit=None, offset=None):
        """
        Pulls ALL adcampaigns for a Facebook ads account

        :param int adaccount_id: The id corresponding to the Facebook account to pull adcampaigns from.
        :param boolean include_deleted: A flag that determines whether or not to include deleted adcampaigns in the resultset
        :param int limit: A limit for the number of adcampaign objects to request
        :param int offset: An offset for the adcampaign resultset

        :rtype [ AdCampaign ]: A list of the AdCampaigns found.
        """
        if not adaccount_id or type(adaccount_id) not in (str, unicode):
            raise FacebookException("Must pass an adaccount_id of type in ( str, unicode ) to this call")

        if 'act_' not in adaccount_id:
            adaccount_id = 'act_' + adaccount_id

        params = {}
        if include_deleted:
            params["include_deleted"] = "true"
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)

        return self._fb.get_list_from_fb(adaccount_id, self, params, fields=self.FIELDS_NAME_LIST)

    def find_by_adgroup_id(self, adgroup_id):
        """
        Retriees the AdCampaign object associated with this AdGroup

        :param int adgroup_id: The id for the adgroup

        :rtype: AdCampaign the AdCampaign object associated with this AdGroup
        """
        from pyfacebook.api.adgroup import AdGroup
        if not adgroup_id:
            raise FacebookException("Must set an id before making this call")
        adgroup = AdGroup(fb=self._fb).find_by_id(adgroup_id)
        campaign_id = adgroup.campaign_id
        return self._fb.get_one_from_fb(campaign_id, self, fields=self.FIELDS_NAME_LIST)

    def find_by_id(self, adcampaign_id):
        """
        Retrieves the AdCampaign object corresponding to the object id passed

        :param int adcampaign_id: The id for the adcampaign from the perspective of Facebook

        :rtype AdCampaign:
        """
        return self._fb.get_one_from_fb(adcampaign_id, self, fields=self.FIELDS_NAME_LIST)

    def find_by_ids(self, adcampaign_ids):
        """
        Retreives a list of AdCampaign objects from a list of adcampaign IDs subject to Facebook's max limit/batch size

        :param list adcampaign_ids: The list of adcampaign IDs we are searching for

        :rtype [AdCampaign]: A list of AdCampaign objects found.

        """
        return self._fb.get_many_from_fb(adcampaign_ids, self, fields=self.FIELDS_NAME_LIST)
