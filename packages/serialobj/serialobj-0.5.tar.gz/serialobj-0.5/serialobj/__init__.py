"""Library to auto-generate JSON-compatible objects."""
from collections import Iterable
import six

try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap

try:
    import ujson as json
except ImportError:
    import json


class Error(Exception):
    """Base class of all errors raised by the jsonobj module."""


class DefinitionError(Error):
    """Error raised during class definition."""


class InvalidTypeError(Error):
    """Type differs from spec."""


class BadValueError(Error):
    """Unexpected value."""


class StrictError(Error):
    """Error raised only when __strict__ == True."""


class KeyMismatchError(StrictError):
    """Deserialized object doesn't match the expected keys"""


class NoneAttributeError(StrictError):
    """Some attributes of the class are empty."""


class UnknownKeysError(StrictError):
    """The deserialized data contains unknown keys."""


if six.PY3:
    NATIVE_TYPES = (int, str, float, bool, dict)
else:
    NATIVE_TYPES = (int, str, unicode, float, bool, dict)


class _ListDeserializer(object):
    def __init__(self, cls_):
        self.cls_ = cls_

    def deserialize(self, data, strict=None):
        if data is None:
            return None
        if type(data) in NATIVE_TYPES:
            raise InvalidTypeError("Expected a sequence, got: {!r}"
                                   .format(data))
        if not isinstance(data, Iterable):
            raise InvalidTypeError("Expected an iterable object, got {!r}"
                                   .format(data))
        return [self.cls_.deserialize(elt) for elt in data]

    def serialize(self, lst, strict=None):
        if hasattr(self.cls_, 'serialize'):
            return [self.cls_.serialize(elt, strict) for elt in lst]
        return list(lst)


class _StaticCheck(object):
    def __init__(self, cls_):
        self.cls_ = cls_
        if six.PY2:
            if cls_ in (str, unicode):
                self.cls_ = six.text_type

    def deserialize(self, data, *args, **kwargs):
        if six.PY2 and self.cls_ is unicode:
            if isinstance(data, str):
                data = data.decode('utf-8')
        if data is not None and not isinstance(data, self.cls_):
            raise InvalidTypeError("Expected {}, got {!r}"
                                   .format(self.cls_.__name__, data))
        return data


class Choice(object):
    def __init__(self, *args):
        self.args = set(args)

    def deserialize(self, data, strict=None):
        if data not in self.args:
            raise BadValueError("Expected one of {!r}, got {!r}"
                                .format(self.args, data))
        return data

    def serialize(self, data, strict=None):
        return self.deserialize(data, strict)


Singleton = Choice


class SerialObjectMeta(type):
    """Metaclass that generates constructor and classmethods from a class's
    __fields__ attribute.
    """
    def __new__(mcs, name, bases, attrs):
        fields = attrs.get('__fields__', {})
        attrs.setdefault('__strict__', False)

        if not isinstance(fields, dict):
            raise DefinitionError(
                "__fields__ attribute of class {} should be a dict, not {}."
                .format(name, type(fields).__name__))

        fields = ChainMap(fields)

        # Inherit fields of base classes
        for base in bases:
            if isinstance(base, SerialObjectMeta):
                fields.maps.extend(getattr(base, '__fields__').maps)

        for key, val in fields.items():
            # Handle syntaxic sugar [SomeClass] that means
            # "a list of instances of SomeClass"
            if val in NATIVE_TYPES:
                val = fields[key] = _StaticCheck(val)
            if isinstance(val, list):
                if len(val) != 1:
                    raise DefinitionError(
                        "Unknown type spec: {!r}".format(val))
                cls_ = val[0]
                if cls_ in NATIVE_TYPES:
                    cls_ = _StaticCheck(cls_)
                if not hasattr(cls_, 'deserialize'):
                    raise DefinitionError(
                        "Can only handle list of classes with a 'deserialize' "
                        "classmethod. Found [{}]"
                        .format(type(cls_))
                    )
                val = fields[key] = _ListDeserializer(cls_)

            # Check all fields have a deserialize method
            if not hasattr(val, 'deserialize'):
                raise DefinitionError(
                    "Field '{}' from class '{}' __fields__ attribute is of "
                    "type {} and doesn't define a deserialize(...) classmethod."
                    .format(key, name, type(val))
                )

        attrs['__fields__'] = fields

        # We define the methods here so it becomes possible to subclass
        # SerialObjMeta to define new metaclasses
        def __init__(self, *args, **kwargs):
            for key in self.__fields__.keys():
                data = kwargs.get(key)
                if isinstance(data, str):
                    data = six.u(data)
                setattr(self, key, data)

        def serialize(self, strict=None):
            """Serialize the object and its descendants in a json-compatible
            dict-and-list structure.

            Optional Args:
                * strict (bool): override the __strict__ attribute during
                serialization.

            Return:
                A json-compatible dict object conforming the __fields__ spec
                for this object.

            """
            strict_ = strict
            if strict_ is None:
                strict_ = self.__strict__
            res = {}
            for key, type_ in self.__fields__.items():
                val = getattr(self, key)
                if val is None:
                    if strict_:
                        raise NoneAttributeError(
                            "[strict] Attribute {} of class {} is None."
                            .format(key, type(self).__name__)
                        )
                elif hasattr(type_, 'serialize'):
                    res[key] = type_.serialize(val, strict)
                elif type(val) in NATIVE_TYPES:
                    res[key] = val
                else:
                    raise InvalidTypeError("Un-serializable object: {!r}"
                                           .format(val))
            return res

        def to_json(self):
            """Serialize a SerialObject to a json string.

            Optional Args:
                * strict (bool): override the __strict__ attribute during
                deserialization.

            Return:
                A json string conforming the __fields__ spec for this object.

            """
            return json.dumps(self.serialize())

        attrs['__init__'] = __init__
        attrs['serialize'] = serialize
        attrs['to_json'] = to_json

        if six.PY2:
            sup = super(SerialObjectMeta, mcs)
        else:
            sup = super()
        return sup.__new__(mcs, name, bases, attrs)

    def deserialize(cls, data, strict=None):
        """Deserialize a dict-and-list structure using the __fields__
        specification.

        Args:
            * data (dict): a dictionary to deserialize to a SerialObject

        Optional Args:
            * strict (bool): override the __strict__ attribute
              of this object during deserialization.

        Return:
            A populated SerialObject instance.

        """
        return cls._deserialize(cls, data, strict)

    @staticmethod
    def _deserialize(cls, data, strict):
        strict_ = strict
        if strict_ is None:
            strict_ = cls.__strict__

        if not isinstance(data, dict):
            raise InvalidTypeError(
                "Class {} expects a dict. Got {!r}"
                .format(cls.__name__, data))
        if strict_:
            fkeys = set(cls.__fields__.keys())
            dkeys = set(data.keys())
            if fkeys != dkeys:
                raise KeyMismatchError(
                    "[strict] Class {} expects keys {!r}. Got {!r}."
                    .format(cls.__name__, fkeys, dkeys))

        kwargs = {
            key: cls.__fields__[key].deserialize(val, strict)
            for key, val in data.items() if key in cls.__fields__
        }
        return cls(**kwargs)

    def from_json(cls, data, strict=None):
        """Deserialize a json string to a SerialObject.

        Args:
            * data (str): the json string to deserialize.

        Optional Args:
            * strict (bool): override the __strict__ attribute during
              deserialization.

        Return:
            A populated SerialObject instance.

        """
        return cls.deserialize(json.loads(data), strict)


@six.add_metaclass(SerialObjectMeta)
class SerialObject(object):
    """A SerialObject is an object that supports serialization from/to
    json-like objects (dicts and lists of builtin types).

    The serialization specification is taken from the __fields__ class
    attribute, which is on the form:

        __fields__: {
            FIELD_NAME: FIELD_SPEC
        }

    A FIELD_NAME is a string, its only constraint is that it should be a valid
    object attribute name.

    FIELD_SPEC can be:
        * Any native type from:
            * str
            * int
            * float
            * bool
            * dict
        * A SerialObject subclass
        * Choice(val1, val2, ...) to form enumerations, values should be of a
          native type (see above).
        * [FIELD_SPEC]: a list of objects depicted by the above specs.

    Additionnally, SerialObjects support a __strict__ boolean class attribute
    (False by default). When __strict__ == True, an exhaustivity check is
    performed during (de-)serialization and missing or unknown keys yield
    errors.

    """
    pass
