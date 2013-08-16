from pyfacebook.api import Model
from tinymodel import FieldDef


class ActionSpec(Model):
    """
    The ActionSpec class represents the action-spec object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/action-specs/
    We extend the functionality in the documentation with custom calls for action-specs
    """
    FIELD_DEFS = [
        FieldDef(title='action.type', required=False, allowed_types=[[unicode], type(None)]),
        FieldDef(title='post', required=False, allowed_types=[unicode]),
        FieldDef(title='post.object', required=False, allowed_types=[unicode, type(None)]),
    ]
