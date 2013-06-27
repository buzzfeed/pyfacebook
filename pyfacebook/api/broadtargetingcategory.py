from pyfacebook.fault import Fault, FacebookException


class BroadTargetingCategoryApi:

    def __init__(self, fb):
        self.__fb = fb

    def find_by_adaccount_id(self, adaccount_id):
        """
        Retrieves BroadTargetingCategory objects associated with this AdAccount

        :param int adaccount_id: The adaccount id

        :rtype: List of BroadTargetingCategory objects contained by this AdAccount

        """
        try:
            if not adaccount_id:
                raise FacebookException("Must set an id before making this call")
            btcs = self.__fb.get_all('/act_' + str(adaccount_id) + '/broadtargetingcategories')
            return [self.__fb.broadtargetingcategory(btc)[0] for btc in btcs], []
        except:
            return [], [Fault()]
