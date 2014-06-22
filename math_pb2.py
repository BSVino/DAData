# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='math.proto',
  package='da.protobuf',
  serialized_pb='\n\nmath.proto\x12\x0b\x64\x61.protobuf\")\n\x06Vector\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\t\n\x01z\x18\x03 \x02(\x02\" \n\x08Vector2D\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\")\n\x06\x45\x41ngle\x12\t\n\x01p\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\t\n\x01r\x18\x03 \x02(\x02\"J\n\x04\x41\x41\x42\x42\x12 \n\x03min\x18\x01 \x02(\x0b\x32\x13.da.protobuf.Vector\x12 \n\x03max\x18\x02 \x02(\x0b\x32\x13.da.protobuf.Vector\"|\n\x03TRS\x12(\n\x0btranslation\x18\x01 \x02(\x0b\x32\x13.da.protobuf.Vector\x12%\n\x08rotation\x18\x02 \x02(\x0b\x32\x13.da.protobuf.EAngle\x12$\n\x07scaling\x18\x03 \x02(\x0b\x32\x13.da.protobuf.Vector')




_VECTOR = descriptor.Descriptor(
  name='Vector',
  full_name='da.protobuf.Vector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='x', full_name='da.protobuf.Vector.x', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='y', full_name='da.protobuf.Vector.y', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='z', full_name='da.protobuf.Vector.z', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=27,
  serialized_end=68,
)


_VECTOR2D = descriptor.Descriptor(
  name='Vector2D',
  full_name='da.protobuf.Vector2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='x', full_name='da.protobuf.Vector2D.x', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='y', full_name='da.protobuf.Vector2D.y', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=70,
  serialized_end=102,
)


_EANGLE = descriptor.Descriptor(
  name='EAngle',
  full_name='da.protobuf.EAngle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='p', full_name='da.protobuf.EAngle.p', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='y', full_name='da.protobuf.EAngle.y', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='r', full_name='da.protobuf.EAngle.r', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=104,
  serialized_end=145,
)


_AABB = descriptor.Descriptor(
  name='AABB',
  full_name='da.protobuf.AABB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='min', full_name='da.protobuf.AABB.min', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='max', full_name='da.protobuf.AABB.max', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=147,
  serialized_end=221,
)


_TRS = descriptor.Descriptor(
  name='TRS',
  full_name='da.protobuf.TRS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='translation', full_name='da.protobuf.TRS.translation', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rotation', full_name='da.protobuf.TRS.rotation', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='scaling', full_name='da.protobuf.TRS.scaling', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=223,
  serialized_end=347,
)

_AABB.fields_by_name['min'].message_type = _VECTOR
_AABB.fields_by_name['max'].message_type = _VECTOR
_TRS.fields_by_name['translation'].message_type = _VECTOR
_TRS.fields_by_name['rotation'].message_type = _EANGLE
_TRS.fields_by_name['scaling'].message_type = _VECTOR
DESCRIPTOR.message_types_by_name['Vector'] = _VECTOR
DESCRIPTOR.message_types_by_name['Vector2D'] = _VECTOR2D
DESCRIPTOR.message_types_by_name['EAngle'] = _EANGLE
DESCRIPTOR.message_types_by_name['AABB'] = _AABB
DESCRIPTOR.message_types_by_name['TRS'] = _TRS

class Vector(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VECTOR
  
  # @@protoc_insertion_point(class_scope:da.protobuf.Vector)

class Vector2D(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VECTOR2D
  
  # @@protoc_insertion_point(class_scope:da.protobuf.Vector2D)

class EAngle(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EANGLE
  
  # @@protoc_insertion_point(class_scope:da.protobuf.EAngle)

class AABB(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AABB
  
  # @@protoc_insertion_point(class_scope:da.protobuf.AABB)

class TRS(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TRS
  
  # @@protoc_insertion_point(class_scope:da.protobuf.TRS)

# @@protoc_insertion_point(module_scope)