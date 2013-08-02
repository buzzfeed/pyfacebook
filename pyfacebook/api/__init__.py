# python-dateutil-2.1.tar.gz
import copy
import pytz
import collections
import warnings
import random as r
import string as s
import json as j
from datetime import datetime, timedelta
from decimal import Decimal
from importlib import import_module

from dateutil import parser as date_parser


class SentinelValue(object):
    """
    A generic class to determine whether an optional value has been actually passed to a function/method.
    Arguments of type SentinelValue are meant to be ignored for any action taken in the function/method.

    Usage:

    def my_function(a, b=SentinelValue()):
        # do something
    """

    def __nonzero__(self):
        return False
    pass

UNDEFINED = SentinelValue()


class ValidationError(Exception):
    pass


class FieldDef(object):
    """
    This class is an abstract representation of a field on a ValidatedModel.
    Instantiated objects of this class hold class-level about the FIELD_DEFS tuple on a ValidatedModel definition.
    This meta-data is used for field validation, and allows us to generalize field-level operations such as
    serialization, deserialization, etc.

    """

    def __init__(self, title, required=True, validate=True, allowed_types=None, relationship='attribute', default=None, force_default=False, choices=[]):
        """
        Creates an instance of a FieldDef object

        :param str title: The title of the field
        :param bool required: True indicates a required field, False indicates an optional field
        :param bool validate: Indicates that a field is validated during Model initialization.
        :param [ class | {class: class} | [class] | (class,) | {class,} ] allowed_types: An array of allowed types for the field
        :param str relationship: Specifies the type of relationship, for related model fields.
                                 Must be one of ['has_one' | 'has_many' | 'attribute']
        :param function default: A function to calculate the default value of a field.
                                 This function should take a single argument of type ValidatedModel
        :param bool force_default: If true, forces the default function every time values are set

        Allowed types are represented by Python class definitions. Valid classes include
        all Python built-in types listed in ValidatedModel.SUPPORTED_BUILTINS. Also valid are
        nested collections of supported types, structured as dicts, lists, tuples, or sets.
        For example (int,), [[str]], and {str: float} are all valid types.

        User-defined classes are also allowed as valid types, as long as they support all
        of the methods listed in ValidatedModel.SUPPORTED_METHODS. If you want to use your own class
        as a field type but don't want to bother validating it, then just pass validated=False.
        Unvalidated FIELD_DEFS are allowed but are not guaranteed to work with the
        generalized field-level functionality provided in ValidatedModel. Use caution.

        User-defined classes may also be represented as fully-qualified import strings
        (i.e. 'discotech.api.MyClass') rather than class definitions. In this case, the
        import string is evaluated and replaced with the actual class definition when your model is initialized.
        Import errors on optional FIELD_DEFS are treated instead as warnings, and the field is removed from the model.

        This functionality allows you to use other models as foreign keys without necessarily coupling the models together.

        """
        if relationship not in ('has_one', 'has_many', 'attribute'):
            raise AttributeError("Bad value for field relationship: " + str(relationship) +
                                 "\nMust be one of the following: 'has_one', 'has_many', 'attribute'")
        self.title = title
        self.required = required
        self.validate = validate
        self.allowed_types = allowed_types
        self.relationship = relationship
        self.default = default
        self.force_default = force_default
        self.choices = choices


class Field(object):
    """
    This class is an instance-level representation of a field on a ValidatedModel.
    Instantiated objects of this class hold validation data about the FIELDS tuple on a ValidatedModel.

    """

    def __init__(self, title):
        """
        Creates an instance of a Field object

        :param str title: The title of the field

        """
        self.title = title
        self.was_validated = False
        self.last_validated_value = None

    def is_valid(self, current_value):
        """
        Returns whether or not a field is valid, given the current value of the field.
        Fields start as invalid, and previously validated fields become invalidated when their values change.

        :param object current_value: The current value of the field.
        :rtype bool: Flag indicating whether the field is currently valid or not.
        """

        return bool(self.was_validated and current_value == self.last_validated_value)


class ValidatedModel(object):
    """
    Extends the rose.model.Model class to include datatypes and related functionality

    A subset of the standard Python built-in types are supported by this class. These are listed as keys of the SUPPORTED_BUILTINS attribute.
    Each supported built-in requires some corresponding meta-data which describes how these built-ins are used by the methods listed in SUPPORTED_METHODS.
    This meta-data is expressed in the form of lambda functions, listes as values of each SUPPORTED_BUILTINS entry.

    Either or both of the SUPPORTED_BUILTINS or the SUPPORTED_METHODS attributes can be extended or overwritten.
    But be careful! Extending the SUPPORTED_METHODS attribute will also require you to extend the SUPPORTED_BUILTINS attribute as well.
    If you add support for any new types OR methods, and neglect to define new lambda functions in SUPPORTED_BUILTINS then a fatal error will be raised on validation.
    It's recommended that any new SUPPORTED_METHODS that you define accept **kwargs in the method definition, to avoid parameter errors.

    :param objects kwargs: The initial values of each field can be passed in as a keyword parameter.
                           Values are not validated until you call Model.validate()

    """

    COLLECTION_TYPES = (dict, list, tuple, set)
    VALIDATED_CLASSES = []
    NATIVE_ATTRIBUTES = ('NATIVE_ATTRIBUTES',
                         'FIELD_DEFS',
                         'FIELDS',
                         'COLLECTION_TYPES',
                         'SUPPORTED_METHODS',
                         'SUPPORTED_BUILTINS',
                         'REMOVED_FIELDS',
                         'VALIDATION_FAILURES',
                         'VALIDATED_CLASSES',
                         'JSON_FAILURES')

    def __init__(self, **kwargs):
        """
        Checks validity of type definitions and initializes the Model

        """
        self.VALIDATION_FAILURES = []
        self.JSON_FAILURES = []
        self.FIELDS = []
        self.REMOVED_FIELDS = []

        if getattr(self, 'SUPPORTED_METHODS', None) is None:
            self.SUPPORTED_METHODS = ['to_json', 'from_json', 'random']
        if getattr(self, 'SUPPORTED_BUILTINS', None) is None:
            self.SUPPORTED_BUILTINS = {
                type(None): {
                    'to_json': lambda this_value: j.dumps(this_value),
                    'from_json': lambda this_value=None: None,
                    'random': lambda this_value=None: None,
                },
                int: {
                    'to_json': lambda this_value: j.dumps(this_value),
                    'from_json': lambda this_value: j.loads(this_value),
                    'random': lambda: r.randint(0, 1000),
                },
                long: {
                    'to_json': lambda this_value: j.dumps(this_value),
                    'from_json': lambda this_value: long(j.loads(this_value)),
                    'random': lambda: long(r.randint(0, 1000)),
                },
                float: {
                    'to_json': lambda this_value: j.dumps(this_value),
                    'from_json': lambda this_value: j.loads(this_value),
                    'random': lambda: r.uniform(0, 1000),
                },
                Decimal: {
                    'to_json': lambda this_value: j.dumps(float(this_value)),
                    'from_json': lambda this_value: Decimal(j.loads(str(this_value))),
                    'random': lambda: Decimal(r.uniform(0, 1000)),
                },
                bool: {
                    'to_json': lambda this_value: j.dumps(this_value),
                    'from_json': lambda this_value: j.loads(this_value),
                    'random': lambda: r.choice([True, False]),
                },
                str: {
                    'to_json': lambda this_value: str(j.dumps(this_value)),
                    'from_json': lambda this_value: str(j.loads(this_value)),
                    'random': lambda: ''.join(r.choice(s.printable) for x in range(r.randint(0, 25))).encode("ascii"),
                },
                unicode: {
                    'to_json': lambda this_value: unicode(j.dumps(this_value)),
                    'from_json': lambda this_value: unicode(j.loads(this_value)),
                    'random': lambda: ''.join(unichr(r.randint(160, 887)) for x in range(r.randint(0, 25))).encode("utf-8"),
                },
                datetime: {
                    'to_json': lambda this_value: j.dumps(this_value, default=lambda obj: obj.replace(microsecond=0).isoformat()),
                    'from_json': lambda this_value: date_parser.parse(j.loads(this_value)),
                    'random': lambda: (datetime.utcnow() - timedelta(seconds=r.randrange(2592000))).replace(tzinfo=pytz.utc),
                },
                dict: {
                    'to_json': lambda this_value: '{' + ','.join([self.__field_to_json(key) + ': ' + self.__field_to_json(value) for (key, value) in this_value.items()]) + '}',
                    'from_json': lambda key_type, value_type, this_value, this_field_def: {self.__field_from_json([key_type], key, this_field_def): self.__field_from_json([value_type], value, this_field_def) for (key, value) in this_value.items()},
                    'random': lambda key_type, value_type, model_recursion_depth, this_field_def: {self.__random_field(key_type, model_recursion_depth, this_field_def): self.__random_field(value_type, model_recursion_depth, this_field_def) for x in range(r.randint(0, 5))},
                },
                list: {
                    'to_json': lambda this_value: '[' + ','.join([self.__field_to_json(element) for element in this_value]) + ']',
                    'from_json': lambda element_type, this_value, this_field_def: [self.__field_from_json([element_type], element, this_field_def) for element in this_value],
                    'random': lambda element_type, model_recursion_depth, this_field_def: [self.__random_field(element_type, model_recursion_depth, this_field_def) for x in range(r.randint(1, 5))]
                },
                tuple: {
                    'to_json': lambda this_value: '[' + ','.join([self.__field_to_json(element) for element in this_value]) + ']',
                    'from_json': lambda element_type, this_value, this_field_def: tuple([self.__field_from_json([element_type], element, this_field_def) for element in this_value]),
                    'random': lambda element_type, model_recursion_depth, this_field_def: tuple([self.__random_field(element_type, model_recursion_depth, this_field_def) for x in range(r.randint(1, 5))])
                },
                set: {
                    'to_json': lambda this_value: '[' + ','.join([self.__field_to_json(element) for element in this_value]) + ']',
                    'from_json': lambda element_type, this_value, this_field_def: set([self.__field_from_json([element_type], element, this_field_def) for element in this_value]),
                    'random': lambda element_type, model_recursion_depth, this_field_def: set([self.__random_field(element_type, model_recursion_depth, this_field_def) for x in range(r.randint(1, 5))])
                },
            }

        if type(self) not in self.VALIDATED_CLASSES:
            self.__validate_builtin_method_support()
            self.__validate_field_types()
            self.VALIDATED_CLASSES.append(type(self))

        self.FIELDS = map(lambda field_def: Field(title=field_def.title), self.FIELD_DEFS)

        # add id fields for has_one relationships
        for field_def in [fd for fd in self.FIELD_DEFS if fd.relationship == 'has_one']:
            self.FIELDS.append(FieldDef(title=(field_def.title + '_id'),
                                        required=False,
                                        allowed_types=[long, int, unicode, str, type(None)]))

        # add ids fields for has_many relationships
        for field_def in [fd for fd in self.FIELD_DEFS if fd.relationship == 'has_many']:
            self.FIELDS.append(FieldDef(title=(field_def.title + '_ids'),
                                        required=False,
                                        allowed_types=[[long], [int], [unicode], [str], type(None)]))

        # set fields based on passed-in values
        [setattr(self, key, value) for key, value in kwargs.items() if value != UNDEFINED]

        # set defaults
        default_fields = [field_def for field_def in self.FIELD_DEFS if field_def.default and (not hasattr(self, field_def.title) or field_def.force_default)]
        for field in default_fields:
            setattr(self, field.title, field.default(self))

    def __validate_builtin_method_support(self):
        """
        Checks that all of the builtins defined in SUPPORTED_BUILTINS support all of methods defined in SUPPORTED_METHODS
        Raises an Exception if support is missing for any method, on any builtin

        """
        for method in self.SUPPORTED_METHODS:
            for (builtin, builtin_supported_methods) in self.SUPPORTED_BUILTINS.items():
                if method not in builtin_supported_methods:
                    self.VALIDATION_FAILURES.append(method + " not supported by builtin type: " + str(builtin))
        if self.VALIDATION_FAILURES:
            raise ValidationError("Supported methods validation failed on ValidatedModel of class " + str(type(self)) + "\nUnsupported methods:\n" + "\n".join(self.VALIDATION_FAILURES))

    def __validate_field_types(self):
        """
        Checks that all of the type definitions fields defined in the FIELD_DEFS array are structured correctly,
        and that they contain valid builtins and user-defined classes. Classes defined with input strings are evaluated and replaced.

        Raises an Exception if any invalid fields are found.

        """
        if getattr(self, 'FIELD_DEFS', False):
            duplicate_field_titles = [x for x, y in collections.Counter([field.title for field in self.FIELD_DEFS]).items() if y > 1]
            if duplicate_field_titles:
                raise ValidationError("Duplicate field titles in FIELD_DEFS for ValidatedModel " + str(self) + ": " + " ".join(duplicate_field_titles))
            for field in self.FIELD_DEFS:
                if not field.title:
                    raise ValidationError("Field validation failed on ValidatedModel of class " + str(type(self)) + ". Field name cannot be empty!")
                for index, field_type in enumerate(field.allowed_types):
                    field.allowed_types[index] = self.__substitute_class_refs(field_name=field.title, required=field.required, field_type=field_type)

            new_fields_list = []
            for key, val in enumerate(self.FIELD_DEFS):
                if val.title in self.REMOVED_FIELDS:
                    del self.FIELD_DEFS[key]

            for field_def in self.FIELD_DEFS:
                for field_type in field_def.allowed_types:
                    if field_def.validate:
                        self.__validate_type(field_name=field_def.title, field_type=field_type)
            if self.VALIDATION_FAILURES:
                raise ValidationError("Field types validation failed on ValidatedModel of class " + str(type(self)) + "\nInvalid types:\n" + "\n".join(self.VALIDATION_FAILURES))
        else:
            raise ValidationError("FIELD_DEFS list is missing or empty on ValidatedModel of class " + str(type(self)))

    def __validate_type(self, field_name, field_type):
        """
        Checks the validity of a field type. Collection types (i.e. dict, list, tuple and set) are handled recursively.
        Any failures encountered are added to the private attribute VALIDATION_FAILURES

        :param str field_name: The name of the field we are validating
        :param class | {class: class} | [class] | (class,) | {class,} field_type: The field type, as a Python class definition

        """

        if type(field_type) in (list, tuple, set):
            for element in field_type:
                self.__validate_type(field_name=field_name, field_type=element)
        elif type(field_type) == dict:
            for key, value in field_type.iteritems():
                self.__validate_type(field_name=field_name, field_type=key)
                self.__validate_type(field_name=field_name, field_type=value)
        elif type(field_type) == type:
            if field_type not in self.SUPPORTED_BUILTINS:
                for required_method in self.SUPPORTED_METHODS:
                    if required_method not in dir(field_type):
                        self.VALIDATION_FAILURES.append(field_name + ": " + str(field_type) + " missing required method " + required_method)
        else:
            self.VALIDATION_FAILURES.append(field_name + ": " + str(type(field_type)) + " not a recognized type")

    def __substitute_class_refs(self, field_name, required, field_type):
        """
        Recurses through field_type and replaces references to classes with the actual class definitions.
        An error is raised if the class module cannot be found. In the case of an optional FIELD_DEF, a warning is raised
        instead of an error, and the field is removed from the Model.

        :param str field_name: The name of the field
        :param bool required: True indicates a required field. False indicates and optional field
        :param class | {class: class} | [class] | (class,) | {class,} field_type: The field type, as a Python class definition

        """
        if type(field_type) in self.COLLECTION_TYPES and len(field_type) > 1:
            raise Exception(str(type(field_type)) + " field types can only have one element: " + field_name + " on ValidatedModel " + str(type(self)))
        elif type(field_type) == list:
            return [self.__substitute_class_refs(field_name=field_name, required=required, field_type=field_type[0])]
        elif type(field_type) == tuple:
            return tuple([self.__substitute_class_refs(field_name=field_name, required=required, field_type=field_type[0])])
        elif type(field_type) == set:
            return set([self.__substitute_class_refs(field_name=field_name, required=required, field_type=iter(field_type).next())])
        elif type(field_type) == dict:
            key, value = field_type.items()[0]
            return_key = self.__substitute_class_refs(field_name=field_name, required=required, field_type=key)
            return_value = self.__substitute_class_refs(field_name=field_name, required=required, field_type=value)
            return {return_key: return_value}
        elif type(field_type) == str:
            this_module_name = ""
            this_class_name = ""
            try:
                this_module_name, this_class_name = field_type.rsplit(".", 1)
                this_module = import_module(this_module_name)
                return getattr(this_module, this_class_name)
            except ImportError:
                if required:
                    raise Exception("Tried to import non-existent module " + this_module_name + " on field " + field_name + " of ValidatedModel " + str(type(self)))
                else:
                    warnings.warn("Tried to import non-existent module " + this_module_name + " on field " + field_name + " of ValidatedModel " + str(type(self)) + "\nThis field will be removed from the model.")
                    self.REMOVED_FIELDS.append(field_name)
                    return field_type
            except AttributeError:
                if required:
                    raise Exception("Tried to access non-existent class " + field_type + " on field " + field_name + " of ValidatedModel " + str(type(self)))
                else:
                    warnings.warn("Tried to access non-existent class " + field_type + " on field " + field_name + " of ValidatedModel " + str(type(self)) + "\nThis field will be removed from the model.")
                    self.REMOVED_FIELDS.append(field_name)
                    return field_type
            except Exception, e:
                raise e
        else:
            return field_type

    def __validate_field_value(self, this_field, original_value, allowed_types, value):
        """
        A field-level validation method that checks the value of the field against the field's allowed_types

        :param Field this_field: The field whose validity we are checking
        :param original_value: The data we are validating. This is so we can keep its structure across recursive calls
        :param [class | {class: class} | [class] | (class,) | {class,}] allowed_types: The allowed data types, as an array of Python class definitions
        :param object value: The value of the field
        :rtype bool: True indicates the field's value is valid, False indicates that it is not

        """

        valid = False

        if type(value) in self.COLLECTION_TYPES:
            valid_allowed_types = [x for x in allowed_types if type(x) == type(value)]
            if valid_allowed_types:
                if value and type(value) == dict:
                    key_valid = self.__validate_field_value(this_field, original_value, map(lambda x: x.keys()[0], valid_allowed_types), value.keys()[0])
                    value_valid = self.__validate_field_value(this_field, original_value, map(lambda x: x.values()[0], valid_allowed_types), value.values()[0])
                    valid = key_valid and value_valid
                elif value:
                    valid = self.__validate_field_value(this_field, original_value, map(lambda x: iter(x).next(), valid_allowed_types), iter(value).next())
                else:
                    # value is an empty collection type, but this is allowed
                    valid = True
        else:
            if type(value) in allowed_types:
                valid = True

        if valid:
            this_field.last_validated_value = original_value

        this_field.was_validated = valid
        return valid

    def __field_from_json(self, allowed_types, json_value, this_field_def=None):
        """
        Generates an instance of a specified type, with a value specified by a passed-in JSON object.
        Since the model has already passed validation, we can assume that allowed_types are either one of the SUPPORTED_BUILTINS or a valid user-defined type.
        Be aware that this assumption may not hold true if the field was set to validate=False

        :param [class | {class: class} | [class] | (class,) | {class,}] allowed_types: The allowed types of the object to generate, as an array of Python class definitions
        :param str | int | dict | list | bool | None json_value: Either a JSON-formatted string containing the value of the object we are generating,
                                                                 or the value itself as an int, dict, list, bool or NoneType.
        :param FieldDef this_field_def: The field that we are generating a random value for

        :rtype object: An instance of this_type, with value specified by json_value

        """
        type_of_value = type(json_value)

        if type_of_value == dict:
            # Use first allowed dict type or user-defined type
            first_usable_type = next(iter([allowed_type for allowed_type in allowed_types if (type(allowed_type) == dict or allowed_type not in self.SUPPORTED_BUILTINS)]), None)
            if type(first_usable_type) == dict:
                (key_type, value_type) = first_usable_type.items()[0]
                return self.SUPPORTED_BUILTINS[dict]['from_json'](key_type, value_type, json_value, this_field_def)

            elif first_usable_type:
                # Assume we are dealing with a valid user-defined type
                return first_usable_type().from_json(model_as_json=json_value, preprocessed=True)
            else:
                self.JSON_FAILURES.append("from_json translation error in " + this_field_def.title + " field: JSON 'object' type not supported by FieldDef.allowed_types")
                return None
        elif type_of_value in self.COLLECTION_TYPES:
            # Use first allowed iterable type
            first_usable_type = next(iter([allowed_type for allowed_type in allowed_types if (type(allowed_type) in (list, tuple, set))]), None)
            if first_usable_type:
                element_type = iter(first_usable_type).next()
                return self.SUPPORTED_BUILTINS[type(first_usable_type)]['from_json'](element_type, json_value, this_field_def)
            else:
                self.JSON_FAILURES.append("from_json translation error in " + this_field_def.title + " field: JSON 'array' type not supported by FieldDef.allowed_types")
                return None
        elif type_of_value == unicode:
            # Use first allowed non-collection type
            first_usable_type = next(iter(filter(lambda t: (t in set(self.SUPPORTED_BUILTINS) - set(self.COLLECTION_TYPES)) or issubclass(t, ValidatedModel), allowed_types)), None)

            if first_usable_type:
                if issubclass(first_usable_type, ValidatedModel):
                    try:
                        return first_usable_type().from_json(json_value, do_validation=False)
                    except ValueError:
                        self.JSON_FAILURES.append("from_json translation error in " + this_field_def.title + " field: JSON 'string | number | true | false | null' type not supported by ModelField.allowed_types")
                        return None
                if not '"' in json_value:
                    tmp = json_value
                    json_value = '"' + json_value + '"'
                return self.SUPPORTED_BUILTINS[first_usable_type]['from_json'](json_value)

            else:
                self.JSON_FAILURES.append("from_json translation error in " + this_field_def.title + " field: JSON 'string | number | true | false | null' type not supported by FieldDef.allowed_types")
                return None
        else:
            # No further translation necessary, but did we translate to an allowed type?
            if type_of_value in allowed_types:
                return json_value
            else:
                # Did not translate to an allowed type. Cast it back to JSON, find the allowed type, and translate to that.
                first_usable_type = next(iter([allowed_type for allowed_type in allowed_types]))
                return self.SUPPORTED_BUILTINS[first_usable_type]['from_json'](j.dumps(json_value))

    def __field_to_json(self, this_value):
        """
        Generates JSON-formatted string representation of a field value. Nested collection types are generated by recursion.
        Since the model has already passed validation, we can assume that type(this_value) is either one of the SUPPORTED_BUILTINS or a valid user-defined type.
        Be aware that this assumption may not hold true if the field was set to validate=False

        :param object this_value: The current value of the field as a Python object.

        :rtype str: A JSON-formatted string representation of the field value

        """

        type_of_value = type(this_value)

        if type_of_value in self.SUPPORTED_BUILTINS:
            return self.SUPPORTED_BUILTINS[type_of_value]['to_json'](this_value)
        else:
            # Assume we are dealing with a valid user-defined type
            return this_value.to_json()

    def __random_field(self, this_type, model_recursion_depth=1, this_field_def=None):
        """
        Generates a randomly-valued instance of a specified type. Nested collection types are generated by recursion.
        Since the model has already passed validation, we can assume that this_type is either one of the SUPPORTED_BUILTINS or a valid user-defined type.
        Be aware that this assumption may not hold true if the field was set to validate=False

        :param class | {class: class} | [class] | (class,) | {class,} this_type: The type of object to generate, as a Python class definition
        :param int model_recursion_depth: The number of levels to recurse when a FIELD entry references another ValidatedModel class.
                                          We require this in order to avoid infinite recursion on cyclical references.
        :param FieldDef this_field_def: The field that we are generating a random value for

        :rtype object: A randomly-valued instance of this_type

        """

        type_of_type = type(this_type)

        if this_field_def.choices:
            return r.choice(choices)
        elif type_of_type in (list, tuple, set):
            element_type = iter(this_type).next()
            return self.SUPPORTED_BUILTINS[type_of_type]['random'](element_type, model_recursion_depth, this_field_def)
        elif type_of_type == dict:
            (key_type, value_type) = this_type.items()[0]
            return self.SUPPORTED_BUILTINS[dict]['random'](key_type, value_type, model_recursion_depth, this_field_def)
        elif this_type in self.SUPPORTED_BUILTINS:
            return self.SUPPORTED_BUILTINS[this_type]['random']()
        else:
            if model_recursion_depth > 0:
                # Assume we are dealing with a valid user-defined type
                return this_type().random(model_recursion_depth=(model_recursion_depth - 1))
            else:
                return("This is a dummy value in place of an object of type " + str(this_type) +
                       ". If this is not what you were expecting, then you need to pass a higher model_recursion_depth.")

    def validate(self, validate_model_integrity=True, prior_errors=[], warning_only=False):
        """
        A model-level validation function which checks the following:
            1) The model contains no fields that are not explicitly defined in the FIELDS array
            2) All fields defined with required=True exist
            3) All existing fields contain valid values

        Exceptions are raised if any of the above is not true.

        :param bool validate_model_integrity: If True, this validation also checks that all required fields exist
                                              and also checks that all attributes of the object are contained in the FIELDS list
        :param [str] prior_errors: Optional list of prior errors to append to any validation errors generated
        :param bool warning_only: If True, this validation will raise only warnings instead of Exceptions

        """
        data_validation_errors = []
        instance_attributes = vars(self).copy()

        native_attributes = self.NATIVE_ATTRIBUTES

        for (key, value) in instance_attributes.items():
            if key in native_attributes:
                del instance_attributes[key]

        if not instance_attributes:
            raise ValidationError("Validation Error on " + str(self) + ": Field values do not exist!")
        if not getattr(self, 'FIELDS', False):
            raise ValidationError("Validation Error on " + str(self) + ": FIELDS array does not exist!")

        for field_def in [x for x in self.FIELD_DEFS if x.required]:
            if validate_model_integrity and not field_def.title in instance_attributes:
                data_validation_errors.append("Missing required field_def: " + field_def.title)

        for (title, value) in instance_attributes.items():
            this_field = next((field for field in self.FIELDS if field.title == title), None)
            this_field_def = next((field_def for field_def in self.FIELD_DEFS if field_def.title == title), None)
            if not (this_field_def or '_id' in title):
                if validate_model_integrity:
                    data_validation_errors.append("Field not defined in self.FIELD_DEFS: " + title)
            elif not this_field:
                if validate_model_integrity:
                    data_validation_errors.append("Field not defined in self.FIELDS: " + title)
            elif (this_field_def and this_field_def.validate) and (not this_field.is_valid(value)):
                if not self.__validate_field_value(this_field=this_field, original_value=value, allowed_types=this_field_def.allowed_types, value=value):
                    data_validation_errors.append("Invalid field: " + title + " has type " + str(type(value)) + " but allowed types are " + str(this_field_def.allowed_types))

        errors = prior_errors + data_validation_errors
        if errors:
            if warning_only:
                warnings.warn("Validation Errors on " + str(self) + ":\n" + "\n".join(errors))
            else:
                raise ValidationError("Validation Errors on " + str(self) + ":\n" + "\n".join(errors))

    def from_json(self, model_as_json, preprocessed=False, do_validation=True, warning_only=True, field_overrides=[]):
        """
        Creates an object from its JSON representation
        Simultaneously iterates over the FIELD_DEFS attribute and the passed-in JSON representation
        to translate each JSON field value into its corresponding Python FIELD_DEFS type.

        We also assume that model_as_json is formatted as a JSON dict,
        and that the keys of this dict exactly match the keys of the FIELD_DEFS attribute

        Please note that JSON supports ONLY STRINGS AS DICT KEYS!
        Dict-type fields with key types other than str are not guaranteed to work with this method.

        If multiple allowed_types are specified for a field, then the first usable type is the one used for JSON translation.
        If you wish to specify an allowed_types ordering that differs from the one in your model's FIELD_DEFS attribute,
        then you can do so using the field_overrides parameter.

        :param str model_as_json: A representation of the model in JSON format
        :param bool preprocessed: A flag indicating whether model_as_json has already been through a JSON preprocessor
        :param bool do_validation: A flag indicating whether the resulting model should be validated before returning
        :param bool warning_only: If True, any validation errors produce only warnings instead of Exceptions.
        :param [FieldDef] field_overrides: An optional list of FeildDef objects, to be used in favor of
                                             the standard list specified in your model's FIELDS_DEFS attribute. Fields are overridden by title.

        :rtype ValidatedModel: An instance of the ValidatedModel with values assigned according to model_as_json.

        """
        self.JSON_FAILURES = []
        json_fields = {}

        if not preprocessed:
            # Assume that the base JSON object is formatted as a dict.
            json_fields = j.loads(model_as_json)
        else:

            json_fields = model_as_json

        for (json_field_name, json_field_value) in json_fields.items():
            this_field_def = (next(iter([x for x in field_overrides if x.title == json_field_name]), None) or
                              next(iter([x for x in self.FIELD_DEFS if x.title == json_field_name]), None))
            if this_field_def:
                setattr(self, json_field_name, self.__field_from_json(allowed_types=this_field_def.allowed_types, json_value=json_field_value,
                                                                      this_field_def=this_field_def))

        # set id fields if they exist
        for field_title in [field.title for field in self.FIELDS if field.title[-3:] == "_id" or field.title[-4:] == "_ids"]:
            if json_fields.get(field_title) and not(hasattr(self, field_title)
                                                    or hasattr(self, field_title[:-3])
                                                    or hasattr(self, field_title[:-4])):
                setattr(self, field_title, json_fields[field_title])

        if do_validation:
            self.validate(prior_errors=self.JSON_FAILURES, warning_only=warning_only)
        return self

    def to_json(self, do_validation=True, warning_only=True, return_dict=False):
        """
        Creates a JSON representation of a model
        Iterates over the FIELD_DEFS attribute to translate each field value into its corresponding JSON representation.

        Please note that JSON supports ONLY STRINGS AS DICT KEYS!
        Dict-type fields with key types other than str are not guaranteed to work with this method.

        :param bool do_validation: A flag indicating whether the resulting model should be validated before returning
        :param bool warning_only: If True, any validation errors produce only warnings instead of Exceptions.

        :rtype str: A JSON-formatted str representation of this model

        """
        json_fields = {}
        object_as_json = ''
        if do_validation:
            self.validate(warning_only=warning_only)
        for field in self.FIELDS:
            try:
                json_fields.update({field.title: self.__field_to_json(this_value=getattr(self, field.title))})
            except AttributeError:
                pass
        object_as_json = '{' + ','.join([('"' + key + '": ' + value) for (key, value) in json_fields.items()]) + '}'

        try:
            object_as_dict = j.loads(object_as_json)
        except:
            if warning_only:
                warnings.warn(str(self) + " could not be translated to a valid JSON object")
            else:
                raise Exception(str(self) + " could not be translated to a valid JSON object")
        else:
            if return_dict:
                return object_as_dict
            else:
                return object_as_json

    def random(self, model_recursion_depth=1):
        """
        Assigns random values to the FIELD_DEFS of the ValidatedModel.
        Iterates over the FIELD_DEFS attribute to generate a random instance of each FIELD_DEFS type.

        :param int model_recursion_depth: The number of levels to recurse when a FIELD entry references another ValidatedModel class.
                                          We require this in order to avoid infinite recursion on cyclical references.
        :rtype ValidatedModel: An instance of the ValidatedModel with random values assigned to all fields.

        """

        for field_def in self.FIELD_DEFS:
            if field_def.title != 'id':
                setattr(self, field_def.title, self.__random_field(this_type=next(iter(field_def.allowed_types)),
                                                                   model_recursion_depth=model_recursion_depth,
                                                                   this_field_def=field_def))

        return self

    def from_foreign_model(self, foreign_model):
        """
        Translates field values from a foreign model to a ValidatedModel.
        Assumes that field names of the foreign model match the field names of the ValidatedModel *exactly*

        :param object foreign_model: The object we want to translate from (e.g. django model, bridge library model, etc)

        """
        if foreign_model is None:
            return None

        set_defaults = []
        for field_def in self.FIELD_DEFS:
            try:
                foreign_value = getattr(foreign_model, field_def.title)
                if foreign_value or not field_def.default:
                    if field_def.relationship == 'has_many':
                        child_class = None
                        # use first usable allowed_type
                        for allowed_type in field_def.allowed_types:
                            if type(allowed_type) == list:
                                child_class = next(iter(allowed_type), None)
                                if child_class not in self.SUPPORTED_BUILTINS:
                                    break
                        if child_class:
                            try:
                                # special case for django
                                if hasattr(foreign_value, "all"):
                                    foreign_value = foreign_value.all()
                                # call from_foreign_model recursively
                                setattr(self, field_def.title, [child_class().from_foreign_model(val) for val in foreign_value])
                            except TypeError:
                                pass
                        else:
                            setattr(self, field_def.title, foreign_value)
                    elif field_def.relationship == 'has_one':
                        # use first usable allowed_type
                        child_class = next(iter([allowed_type for allowed_type in field_def.allowed_types if allowed_type not in self.SUPPORTED_BUILTINS]), None)
                        if child_class and foreign_value:
                            # call from_foreign_model recursively
                            setattr(self, field_def.title, child_class().from_foreign_model(foreign_value))
                        else:
                            setattr(self, field_def.title, foreign_value)
                    else:
                        setattr(self, field_def.title, foreign_value)
                elif field_def.default:
                    set_defaults.extend([field for field in self.FIELD_DEFS if field.title == field_def.title])
            except AttributeError:
                try:
                    if field_def.default:
                        set_defaults.extend([field for field in self.FIELD_DEFS if field.title == field_def.title])
                except AttributeError:
                    pass

        # set defaults
        for field_def in set_defaults:
            if not hasattr(self, field_def.title) or field_def.force_default:
                setattr(self, field_def.title, field_def.default(self))

        # set id fields if they exist
        for field_title in [field.title for field in self.FIELDS if field.title[-3:] == "_id" or field.title[-4:] == "_ids"]:
            if hasattr(foreign_model, field_title) and not(hasattr(self, field_title)
                                                           or hasattr(self, field_title[:-3])
                                                           or hasattr(self, field_title[:-4])):
                foreign_value = getattr(foreign_model, field_title)
                setattr(self, field_title, foreign_value)

        return self

    def replace_refs_with_ids(self):
        """
        Unsets any fields that reference a foreign model, and replaces them with id fields

        :rtype ValidatedModel: Returns self, with ref fields replaced by id fields

        """

        for field_def in self.FIELD_DEFS:
            if field_def.relationship == 'has_one' and getattr(self, field_def.title, False):
                id_field = field_def.title + "_id"
                ref_object = getattr(self, field_def.title)
                setattr(self, id_field, ref_object.id)
                delattr(self, field_def.title)
            elif field_def.relationship == 'has_many' and getattr(self, field_def.title, False):
                ids_field = field_def.title + "_ids"
                ref_objects = getattr(self, field_def.title)
                setattr(self, ids_field, [ref_object.id for ref_object in ref_objects])
                delattr(self, field_def.title)

        return self


class Model(ValidatedModel):
    def __init__(self, **kwargs):
        self._fb = kwargs.pop('fb', None)
        self.NATIVE_ATTRIBUTES += ('_fb',)
        super(Model, self).__init__(**kwargs)

    @property
    def FIELDS_NAME_LIST(self):
        return [f.title for f in self.FIELDS]
