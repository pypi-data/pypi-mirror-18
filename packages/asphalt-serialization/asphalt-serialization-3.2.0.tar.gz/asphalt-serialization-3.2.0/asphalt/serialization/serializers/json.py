import inspect
from collections import OrderedDict
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from typing import Dict, Any, Callable, Optional, Union

from asphalt.core.util import resolve_reference, qualified_name
from typeguard import check_argument_types

from asphalt.serialization.api import CustomizableSerializer
from asphalt.serialization.marshalling import default_marshaller, default_unmarshaller


def default_wrapper(typename: str, state, *, type_key: str = '__type__'):
    return {type_key: typename, 'state': state}


class JSONSerializer(CustomizableSerializer):
    """
    Serializes objects using JSON (JavaScript Object Notation).

    See the :mod:`json` module documentation in the standard library for more information on
    available options.

    Certain options can resolve references to objects:

    * ``encoder_options['default']``
    * ``decoder_options['object_hook']``
    * ``decoder_options['object_pairs_hook']``

    :param encoder_options: keyword arguments passed to :class:`~json.JSONEncoder`
    :param decoder_options: keyword arguments passed to :class:`~json.JSONDecoder`
    :param encoding: the text encoding to use for converting to and from bytes
    :param custom_type_key: magic key that identifies custom types in a JSON object
    :param wrap_state: ``True`` to wrap the marshalled state in an implementation specific
        manner which lets the deserializer automatically deserialize the objects back to
        their proper types; ``False`` to serialize the state as-is without any identifying
        metadata added to it
    """

    __slots__ = ('encoder_options', 'decoder_options', 'encoding', 'custom_type_key', 'wrap_state',
                 '_encoder', '_decoder', '_marshallers', '_unmarshallers')

    def __init__(self, encoder_options: Dict[str, Any] = None,
                 decoder_options: Dict[str, Any] = None, encoding: str = 'utf-8',
                 custom_type_key: str = '__type__', wrap_state: bool = True):
        assert check_argument_types()
        self.encoding = encoding
        self.custom_type_key = custom_type_key
        self.wrap_state = wrap_state
        self._marshallers = OrderedDict()  # class -> (typename, marshaller function)
        self._unmarshallers = OrderedDict()  # typename -> (class, unmarshaller function)

        self.encoder_options = encoder_options or {}

        self.encoder_options['default'] = resolve_reference(self.encoder_options.get('default'))
        self._encoder = JSONEncoder(**self.encoder_options)

        self.decoder_options = decoder_options or {}
        self.decoder_options['object_hook'] = resolve_reference(
            self.decoder_options.get('object_hook'))
        self.decoder_options['object_pairs_hook'] = resolve_reference(
            self.decoder_options.get('object_pairs_hook'))
        self._decoder = JSONDecoder(**self.decoder_options)

    def serialize(self, obj) -> bytes:
        return self._encoder.encode(obj).encode(self.encoding)

    def deserialize(self, payload: bytes):
        payload = payload.decode(self.encoding)
        return self._decoder.decode(payload)

    def register_custom_type(
            self, cls: type, marshaller: Optional[Callable[[Any], Any]] = default_marshaller,
            unmarshaller: Union[Callable[[Any, Any], None],
                                Callable[[Any], Any], None] = default_unmarshaller, *,
            typename: str = None, wrap_state: bool = True) -> None:
        assert check_argument_types()
        typename = typename or qualified_name(cls)

        if marshaller:
            self._marshallers[cls] = typename, marshaller
            self.encoder_options['default'] = self._default_encoder
            self._encoder = JSONEncoder(**self.encoder_options)

        if unmarshaller and self.wrap_state:
            if len(inspect.signature(unmarshaller).parameters) == 1:
                cls = None

            self._unmarshallers[typename] = cls, unmarshaller
            self.decoder_options['object_hook'] = self._custom_object_hook
            self._decoder = JSONDecoder(**self.decoder_options)

    def _default_encoder(self, obj):
        obj_type = obj.__class__
        try:
            typename, marshaller = self._marshallers[obj_type]
        except KeyError:
            raise LookupError('no marshaller found for type "{}"'
                              .format(qualified_name(obj_type))) from None

        state = marshaller(obj)
        if self.wrap_state:
            return {self.custom_type_key: typename, 'state': state}
        else:
            return state

    def _custom_object_hook(self, obj: Dict[str, Any]):
        if len(obj) == 2 and self.custom_type_key in obj:
            typename = obj[self.custom_type_key]
            try:
                cls, unmarshaller = self._unmarshallers[typename]
            except KeyError:
                raise LookupError('no unmarshaller found for type "{}"'.format(typename)) from None

            if cls is not None:
                instance = cls.__new__(cls)
                unmarshaller(instance, obj['state'])
                return instance
            else:
                return unmarshaller(obj['state'])
        else:
            return obj

    @property
    def mimetype(self):
        return 'application/json'
