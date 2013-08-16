from pyfacebook.api import Model

from tinymodel import FieldDef


class Targeting(Model):
    """
    The Targeting class represents an targeting object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/
    """
    FIELD_DEFS = [
        FieldDef(title='genders', required=False, allowed_types=[[int]]),
        FieldDef(title='age_min', required=False, allowed_types=[int]),
        FieldDef(title='age_max', required=False, allowed_types=[int]),
        FieldDef(title='broad_age', required=False, allowed_types=[int]),
        FieldDef(title='countries', required=False, allowed_types=[[unicode]]),
        FieldDef(title='cities', required=False, allowed_types=[[unicode]]),
        FieldDef(title='regions', required=False, allowed_types=[[unicode]]),
        FieldDef(title='radius', required=False, allowed_types=[int]),
        FieldDef(title='keywords', required=False, allowed_types=[[unicode]]),
    ]
