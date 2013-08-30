from pyfacebook.api import Model
from tinymodel import FieldDef
from pyfacebook.fault import FacebookException


class AdStatistic(Model):
    """
    The AdStatistic class represents an adstatistic objects in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adstatistics
    """
    FIELD_DEFS = [
        FieldDef(title='id', required=False, allowed_types=[str]),
        FieldDef(title='account_id', required=False, allowed_types=[long]),
        FieldDef(title='start_time', required=False, allowed_types=[str]),
        FieldDef(title='end_time', required=False, allowed_types=[str]),
        FieldDef(title='impressions', required=False, allowed_types=[unicode]),
        FieldDef(title='clicks', required=False, allowed_types=[unicode]),
        FieldDef(title='spent', required=False, allowed_types=[unicode]),
        FieldDef(title='social_impressions', required=False, allowed_types=[unicode]),
        FieldDef(title='social_clicks', required=False, allowed_types=[unicode]),
        FieldDef(title='social_spent', required=False, allowed_types=[unicode]),
        FieldDef(title='unique_impressions', required=False, allowed_types=[unicode]),
        FieldDef(title='unique_clicks', required=False, allowed_types=[unicode]),
        FieldDef(title='social_unique_impressions', required=False, allowed_types=[int]),
        FieldDef(title='social_unique_clicks', required=False, allowed_types=[unicode]),
    ]

    def find_by_adaccount_id(self, adaccount_id, include_deleted=False):
        """
        Retrieves Statistic objects associated with this AdAccount

        :param int adaccount_id: The adaccount id
        :param bool include_deleted: Includes deleted adstatistics if set to True

        :rtype: AdStatistic object associated with this AdAccount
        """
        resp = {}
        inc_del = 'false'
        if include_deleted:
            inc_del = 'true'
        if not adaccount_id:
            raise FacebookException("Must pass an adaccount_id to this call")
        resp = self._fb.get('/act_' + str(adaccount_id) + '/stats?include_deleted=' + str(inc_del))
        stat = self.__class__(from_json=resp, preprocessed=True)
        return stat, []

    def find_by_adgroup_ids(self, adgroup_ids, adaccount_id, include_deleted=False):
        """
        Retrieves the Statistic object associated with this AdGroup

        :param boolean force_get: Set to true to force retrieval directly from Facebook. Otherwise this method will return objects from memory if available.

        :rtype: AdStatistic object associated with this AdGroup
        """
        if not adgroup_ids:
            raise FacebookException("Must pass an adgroup_id list to this call")

        if not adaccount_id:
            raise FacebookException("Must pass an adaccount_id to this call")

        if str(adaccount_id).find('act_') < 0:
            adaccount_id = 'act_' + str(adaccount_id)

        num_ids = len(adgroup_ids)
        batch = 0
        batchsize = 50
        adstats = []

        while True:
            adgroup_id_batch = adgroup_ids[batch*batchsize:batch*batchsize+batchsize]
            url = '/' + adaccount_id + '/adgroupstats?adgroup_ids=' + '[' + ",".join(map(str, adgroup_id_batch)) + ']'
            if include_deleted:
                url += '&include_deleted=true'
            resp = self._fb.get(url)
            batch = batch + 1
            adstats = adstats + resp['data']

            if batch * batchsize + batchsize > num_ids:
                if num_ids is not batch*batchsize:
                    url = '/' + adaccount_id + '/adgroupstats?adgroup_ids=' + '[' + ",".join(map(str, adgroup_ids[batch*batchsize:num_ids])) + ']'
                    if include_deleted:
                        url += '&include_deleted=true'
                    resp = self._fb.get(url)
                    adstats = adstats + resp['data']
                break

        return [self.__class__(from_json=stat, preprocessed=True) for stat in adstats]

    def find_by_start_time_end_time(self, adaccount_id, start_time, end_time, with_delivery=True, include_deleted=False):
        """
        Retrieves a list of AdStatisics objects for a given AdAccount ID within a datetime range.
        AdStatistics returned will contain ONLY data that was generated within the specified datetime range.

        :param str adaccount_id: The adaccount ID that contains the desired adstatistics
        :param datetime start_time: The start of the datetime range. UTC only.
        :param datetime end_time: The end of the datetime range. UTC only.
        :param boolean with_delivery: If True, the call returns AdStatistics for ONLY AdGroups that generated data within the datetime range
        :param boolean include_deleted: Flag to determine whether we include AdStatistics for deleted AdGroup objects

        :rtype [AdStatistic]: A tuple which includes a list of AdStatistic objects found.

        """
        if not adaccount_id:
            raise FacebookException("Must pass an adaccount_id to this call")
        if (not start_time or not end_time):
            raise FacebookException("Must pass a start_time and end_time to this call")

        if 'act_' not in adaccount_id:
            adaccount_id = 'act_' + adaccount_id

        adstats = []
        base_url = '/' + adaccount_id + '/adgroupstats'
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        params = {"start_time": start_time_str,
                  "end_time": end_time_str}

        if with_delivery:
            params["stats_mode"] = "with_delivery"
        if include_deleted:
            params["include_deleted"] = "true"

        adstats = self._fb.get_all(base_url, params)
        return [self.__class__(from_json=adstat, preprocessed=True) for adstat in adstats]
