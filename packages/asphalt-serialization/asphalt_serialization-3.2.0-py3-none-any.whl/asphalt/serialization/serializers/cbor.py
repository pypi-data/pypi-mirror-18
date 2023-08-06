import inspect
from collections import OrderedDict
from functools import partial
from io import BytesIO
from typing import Dict, Any, Callable, Optional, Union

import cbor2
from asphalt.core.util import qualified_name
from typeguard import check_argument_types

from asphalt.serialization.api import CustomizableSerializer
from asphalt.serialization.marshalling import default_marshaller, default_unmarshaller


@cbor2.shareable_encoder
def _encode_custom_type(encoder: cbor2.CBOREncoder, obj, fp, *, serializer: 'CBORSerializer'):
    obj_type = obj.__class__
    typename, marshaller = serializer.marshallers[obj_type]
    state = marshaller(obj)
    if serializer.wrap_state:
        buf = BytesIO()
        encoder.encode(state, buf)
        serialized_state = buf.getvalue()
        return encoder.encode_semantic(serializer.custom_type_tag, [typename, serialized_state],
                                       fp, disable_value_sharing=True)
    else:
        return encoder.encode(state, fp)


def _decode_custom_type(decoder: cbor2.CBORDecoder, value, fp, shareable_index: Optional[int],
                        *, serializer: 'CBORSerializer'):
    typename, serialized_state = value
    try:
        cls, unmarshaller = serializer.unmarshallers[typename]
    except KeyError:
        raise LookupError('no unmarshaller found for type "{}"'.format(typename)) from None

    buf = BytesIO(serialized_state)
    if cls is not None:
        instance = cls.__new__(cls)
        if shareable_index is not None:
            decoder.shareables[shareable_index] = instance

        state = decoder.decode(buf)
        unmarshaller(instance, state)
        return instance
    else:
        state = decoder.decode(buf)
        return unmarshaller(state)


class CBORSerializer(CustomizableSerializer):
    """
    Serializes objects using CBOR (Concise Binary Object Representation).

    To use this serializer backend, the ``cbor2`` library must be installed.
    A convenient way to do this is to install ``asphalt-serialization`` with the ``cbor``
    extra:

    .. code-block:: shell

        $ pip install asphalt-serialization[cbor]

    .. seealso:: `cbor2 documentation <https://pypi.io/project/cbor2/>`_

    :param encoder_options: keyword arguments passed to ``cbor2.dumps()``
    :param decoder_options: keyword arguments passed to ``cbor2.loads()``
    :param custom_type_tag: semantic tag used for marshalling of registered custom types
    :param wrap_state: ``True`` to wrap the marshalled state in an implementation specific
        manner which lets the deserializer automatically deserialize the objects back to
        their proper types; ``False`` to serialize the state as-is without any identifying
        metadata added to it
    """

    __slots__ = ('encoder_options', 'decoder_options', 'custom_type_tag', 'wrap_state',
                 'marshallers', 'unmarshallers')

    def __init__(self, encoder_options: Dict[str, Any] = None,
                 decoder_options: Dict[str, Any] = None, custom_type_tag: int = 4554,
                 wrap_state: bool = True):
        assert check_argument_types()
        self.encoder_options = encoder_options or {}
        self.decoder_options = decoder_options or {}
        self.custom_type_tag = custom_type_tag
        self.wrap_state = wrap_state
        self.marshallers = OrderedDict()  # class -> (typename, marshaller function)
        self.unmarshallers = OrderedDict()  # typename -> (class, unmarshaller function)

    def serialize(self, obj) -> bytes:
        return cbor2.dumps(obj, **self.encoder_options)

    def deserialize(self, payload: bytes):
        return cbor2.loads(payload, **self.decoder_options)

    def register_custom_type(
            self, cls: type, marshaller: Optional[Callable[[Any], Any]] = default_marshaller,
            unmarshaller: Union[Callable[[Any, Any], None],
                                Callable[[Any], Any], None] = default_unmarshaller, *,
            typename: str = None) -> None:
        assert check_argument_types()
        typename = typename or qualified_name(cls)

        if marshaller:
            self.marshallers[cls] = typename, marshaller
            encoders = self.encoder_options.setdefault('encoders', {})
            encoders[cls] = partial(_encode_custom_type, serializer=self)

        if unmarshaller and self.wrap_state:
            if len(inspect.signature(unmarshaller).parameters) == 1:
                cls = None

            self.unmarshallers[typename] = cls, unmarshaller
            decoders = self.decoder_options.setdefault('semantic_decoders', {})
            decoders[self.custom_type_tag] = partial(_decode_custom_type, serializer=self)

    @property
    def mimetype(self):
        return 'application/cbor'
