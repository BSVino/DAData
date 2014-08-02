# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import math_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='data.proto',
  package='da.protobuf',
  serialized_pb='\n\ndata.proto\x12\x0b\x64\x61.protobuf\x1a\nmath.proto\"\x9f\x06\n\x08GameData\x12\r\n\x05\x64\x65\x62ug\x18\x01 \x01(\x08\x12\x10\n\x08map_name\x18\x02 \x01(\t\x12\x13\n\x0bserver_name\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\x05\x12/\n\tpositions\x18\x05 \x01(\x0b\x32\x1c.da.protobuf.PlayerPositions\x12\x0e\n\x06\x63heats\x18\x06 \x01(\x08\x12+\n\x05kills\x18\x07 \x01(\x0b\x32\x1c.da.protobuf.PlayerPositions\x12,\n\x06\x64\x65\x61ths\x18\x08 \x01(\x0b\x32\x1c.da.protobuf.PlayerPositions\x12\x13\n\x0b\x63onnections\x18\t \x01(\x05\x12\x10\n\x08teamplay\x18\n \x01(\x08\x12\x1a\n\x12thirdperson_active\x18\x0b \x01(\x05\x12\x1c\n\x14thirdperson_inactive\x18\x0c \x01(\x05\x12\x16\n\x0e\x64isconnections\x18\r \x01(\x05\x12\x1f\n\x17unique_players_this_map\x18\x0e \x01(\x05\x12\x12\n\nda_version\x18\x0f \x01(\x05\x12\x19\n\x11\x63haracters_chosen\x18\x10 \x03(\t\x12\x16\n\x0eweapons_chosen\x18\x11 \x03(\x05\x12\x15\n\rskills_chosen\x18\x12 \x03(\x05\x12&\n\x05votes\x18\x13 \x03(\x0b\x32\x17.da.protobuf.VoteResult\x12\x18\n\x10weapons_chosen_s\x18\x14 \x03(\t\x12\x17\n\x0fskills_chosen_s\x18\x15 \x03(\t\x12\x10\n\x08map_time\x18\x16 \x01(\x02\x12\x11\n\tvr_active\x18\x17 \x01(\x05\x12\x13\n\x0bvr_inactive\x18\x18 \x01(\x05\x12\x18\n\x10platform_windows\x18\x19 \x01(\x05\x12\x16\n\x0eplatform_linux\x18\x1a \x01(\x05\x12\x14\n\x0cplatform_osx\x18\x1b \x01(\x05\x12+\n\x0ckill_details\x18\x1c \x03(\x0b\x32\x15.da.protobuf.KillInfo\x12,\n\x0bplayer_list\x18\x1d \x03(\x0b\x32\x17.da.protobuf.PlayerList\"8\n\x0fPlayerPositions\x12%\n\x08position\x18\x01 \x03(\x0b\x32\x13.da.protobuf.Vector\"<\n\nVoteResult\x12\r\n\x05issue\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\x12\x0e\n\x06result\x18\x03 \x01(\x08\"\xb7\x02\n\nPlayerInfo\x12%\n\x08position\x18\x01 \x01(\x0b\x32\x13.da.protobuf.Vector\x12\x0e\n\x06health\x18\x02 \x01(\x05\x12\r\n\x05\x66lags\x18\x03 \x01(\x04\x12\x0e\n\x06weapon\x18\x04 \x01(\t\x12\r\n\x05skill\x18\x05 \x01(\t\x12\x11\n\taccountid\x18\x06 \x01(\r\x12\r\n\x05style\x18\x07 \x01(\x02\x12\x13\n\x0btotal_style\x18\x08 \x01(\x02\x12\r\n\x05kills\x18\t \x01(\r\x12\x0e\n\x06\x64\x65\x61ths\x18\n \x01(\r\x12\x10\n\x08waypoint\x18\x0b \x01(\r\x12/\n\x12objective_position\x18\x0c \x01(\x0b\x32\x13.da.protobuf.Vector\x12\x13\n\x0bslowmo_type\x18\r \x01(\t\x12\x16\n\x0eslowmo_seconds\x18\x0e \x01(\x02\"\x8b\x01\n\x08KillInfo\x12\'\n\x06victim\x18\x01 \x01(\x0b\x32\x17.da.protobuf.PlayerInfo\x12\'\n\x06killer\x18\x02 \x01(\x0b\x32\x17.da.protobuf.PlayerInfo\x12-\n\x10grenade_position\x18\x03 \x01(\x0b\x32\x13.da.protobuf.Vector\"<\n\nPlayerList\x12\x11\n\taccountid\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05style\x18\x03 \x01(\x02\"\xa9\x01\n\x0bServerReply\x12\x14\n\x0c\x64\x61ily_leader\x18\x01 \x01(\t\x12\x1a\n\x12\x64\x61ily_leader_style\x18\x02 \x01(\x02\x12\x15\n\rweekly_leader\x18\x03 \x01(\t\x12\x1b\n\x13weekly_leader_style\x18\x04 \x01(\x02\x12\x16\n\x0emonthly_leader\x18\x05 \x01(\t\x12\x1c\n\x14monthly_leader_style\x18\x06 \x01(\x02*\xbe\x02\n\tKillFlags\x12\x14\n\x10KILL_THIRDPERSON\x10\x00\x12\x0e\n\nKILL_AIMIN\x10\x01\x12\x0f\n\x0bKILL_DIVING\x10\x02\x12\x10\n\x0cKILL_ROLLING\x10\x03\x12\x10\n\x0cKILL_SLIDING\x10\x04\x12\x11\n\rKILL_FLIPPING\x10\x05\x12\x15\n\x11KILL_SUPERFALLING\x10\x06\x12\x13\n\x0fKILL_BY_GRENADE\x10\x07\x12\x11\n\rKILL_BY_BRAWL\x10\x08\x12\x15\n\x11KILL_SKILL_ACTIVE\x10\t\x12\x1b\n\x17KILL_SUPER_SKILL_ACTIVE\x10\n\x12\x12\n\x0eKILL_IS_TARGET\x10\x0b\x12\x16\n\x12KILL_HAS_BRIEFCASE\x10\x0c\x12\x0f\n\x0bKILL_IS_BOT\x10\r\x12\x13\n\x0fKILL_IS_SUICIDE\x10\x0e')

_KILLFLAGS = descriptor.EnumDescriptor(
  name='KillFlags',
  full_name='da.protobuf.KillFlags',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='KILL_THIRDPERSON', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_AIMIN', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_DIVING', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_ROLLING', index=3, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_SLIDING', index=4, number=4,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_FLIPPING', index=5, number=5,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_SUPERFALLING', index=6, number=6,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_BY_GRENADE', index=7, number=7,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_BY_BRAWL', index=8, number=8,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_SKILL_ACTIVE', index=9, number=9,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_SUPER_SKILL_ACTIVE', index=10, number=10,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_IS_TARGET', index=11, number=11,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_HAS_BRIEFCASE', index=12, number=12,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_IS_BOT', index=13, number=13,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KILL_IS_SUICIDE', index=14, number=14,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1652,
  serialized_end=1970,
)


KILL_THIRDPERSON = 0
KILL_AIMIN = 1
KILL_DIVING = 2
KILL_ROLLING = 3
KILL_SLIDING = 4
KILL_FLIPPING = 5
KILL_SUPERFALLING = 6
KILL_BY_GRENADE = 7
KILL_BY_BRAWL = 8
KILL_SKILL_ACTIVE = 9
KILL_SUPER_SKILL_ACTIVE = 10
KILL_IS_TARGET = 11
KILL_HAS_BRIEFCASE = 12
KILL_IS_BOT = 13
KILL_IS_SUICIDE = 14



_GAMEDATA = descriptor.Descriptor(
  name='GameData',
  full_name='da.protobuf.GameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='debug', full_name='da.protobuf.GameData.debug', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='map_name', full_name='da.protobuf.GameData.map_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='server_name', full_name='da.protobuf.GameData.server_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='da.protobuf.GameData.timestamp', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='positions', full_name='da.protobuf.GameData.positions', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='cheats', full_name='da.protobuf.GameData.cheats', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='kills', full_name='da.protobuf.GameData.kills', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='deaths', full_name='da.protobuf.GameData.deaths', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='connections', full_name='da.protobuf.GameData.connections', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='teamplay', full_name='da.protobuf.GameData.teamplay', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='thirdperson_active', full_name='da.protobuf.GameData.thirdperson_active', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='thirdperson_inactive', full_name='da.protobuf.GameData.thirdperson_inactive', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='disconnections', full_name='da.protobuf.GameData.disconnections', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='unique_players_this_map', full_name='da.protobuf.GameData.unique_players_this_map', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='da_version', full_name='da.protobuf.GameData.da_version', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='characters_chosen', full_name='da.protobuf.GameData.characters_chosen', index=15,
      number=16, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weapons_chosen', full_name='da.protobuf.GameData.weapons_chosen', index=16,
      number=17, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='skills_chosen', full_name='da.protobuf.GameData.skills_chosen', index=17,
      number=18, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='votes', full_name='da.protobuf.GameData.votes', index=18,
      number=19, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weapons_chosen_s', full_name='da.protobuf.GameData.weapons_chosen_s', index=19,
      number=20, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='skills_chosen_s', full_name='da.protobuf.GameData.skills_chosen_s', index=20,
      number=21, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='map_time', full_name='da.protobuf.GameData.map_time', index=21,
      number=22, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vr_active', full_name='da.protobuf.GameData.vr_active', index=22,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='vr_inactive', full_name='da.protobuf.GameData.vr_inactive', index=23,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='platform_windows', full_name='da.protobuf.GameData.platform_windows', index=24,
      number=25, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='platform_linux', full_name='da.protobuf.GameData.platform_linux', index=25,
      number=26, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='platform_osx', full_name='da.protobuf.GameData.platform_osx', index=26,
      number=27, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='kill_details', full_name='da.protobuf.GameData.kill_details', index=27,
      number=28, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='player_list', full_name='da.protobuf.GameData.player_list', index=28,
      number=29, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=40,
  serialized_end=839,
)


_PLAYERPOSITIONS = descriptor.Descriptor(
  name='PlayerPositions',
  full_name='da.protobuf.PlayerPositions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='position', full_name='da.protobuf.PlayerPositions.position', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=841,
  serialized_end=897,
)


_VOTERESULT = descriptor.Descriptor(
  name='VoteResult',
  full_name='da.protobuf.VoteResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='issue', full_name='da.protobuf.VoteResult.issue', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='details', full_name='da.protobuf.VoteResult.details', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='result', full_name='da.protobuf.VoteResult.result', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=899,
  serialized_end=959,
)


_PLAYERINFO = descriptor.Descriptor(
  name='PlayerInfo',
  full_name='da.protobuf.PlayerInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='position', full_name='da.protobuf.PlayerInfo.position', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='health', full_name='da.protobuf.PlayerInfo.health', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='flags', full_name='da.protobuf.PlayerInfo.flags', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weapon', full_name='da.protobuf.PlayerInfo.weapon', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='skill', full_name='da.protobuf.PlayerInfo.skill', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='accountid', full_name='da.protobuf.PlayerInfo.accountid', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='style', full_name='da.protobuf.PlayerInfo.style', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='total_style', full_name='da.protobuf.PlayerInfo.total_style', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='kills', full_name='da.protobuf.PlayerInfo.kills', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='deaths', full_name='da.protobuf.PlayerInfo.deaths', index=9,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='waypoint', full_name='da.protobuf.PlayerInfo.waypoint', index=10,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='objective_position', full_name='da.protobuf.PlayerInfo.objective_position', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='slowmo_type', full_name='da.protobuf.PlayerInfo.slowmo_type', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='slowmo_seconds', full_name='da.protobuf.PlayerInfo.slowmo_seconds', index=13,
      number=14, type=2, cpp_type=6, label=1,
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
  serialized_start=962,
  serialized_end=1273,
)


_KILLINFO = descriptor.Descriptor(
  name='KillInfo',
  full_name='da.protobuf.KillInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='victim', full_name='da.protobuf.KillInfo.victim', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='killer', full_name='da.protobuf.KillInfo.killer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='grenade_position', full_name='da.protobuf.KillInfo.grenade_position', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=1276,
  serialized_end=1415,
)


_PLAYERLIST = descriptor.Descriptor(
  name='PlayerList',
  full_name='da.protobuf.PlayerList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='accountid', full_name='da.protobuf.PlayerList.accountid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='da.protobuf.PlayerList.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='style', full_name='da.protobuf.PlayerList.style', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=1417,
  serialized_end=1477,
)


_SERVERREPLY = descriptor.Descriptor(
  name='ServerReply',
  full_name='da.protobuf.ServerReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='daily_leader', full_name='da.protobuf.ServerReply.daily_leader', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='daily_leader_style', full_name='da.protobuf.ServerReply.daily_leader_style', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weekly_leader', full_name='da.protobuf.ServerReply.weekly_leader', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weekly_leader_style', full_name='da.protobuf.ServerReply.weekly_leader_style', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='monthly_leader', full_name='da.protobuf.ServerReply.monthly_leader', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='monthly_leader_style', full_name='da.protobuf.ServerReply.monthly_leader_style', index=5,
      number=6, type=2, cpp_type=6, label=1,
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
  serialized_start=1480,
  serialized_end=1649,
)

_GAMEDATA.fields_by_name['positions'].message_type = _PLAYERPOSITIONS
_GAMEDATA.fields_by_name['kills'].message_type = _PLAYERPOSITIONS
_GAMEDATA.fields_by_name['deaths'].message_type = _PLAYERPOSITIONS
_GAMEDATA.fields_by_name['votes'].message_type = _VOTERESULT
_GAMEDATA.fields_by_name['kill_details'].message_type = _KILLINFO
_GAMEDATA.fields_by_name['player_list'].message_type = _PLAYERLIST
_PLAYERPOSITIONS.fields_by_name['position'].message_type = math_pb2._VECTOR
_PLAYERINFO.fields_by_name['position'].message_type = math_pb2._VECTOR
_PLAYERINFO.fields_by_name['objective_position'].message_type = math_pb2._VECTOR
_KILLINFO.fields_by_name['victim'].message_type = _PLAYERINFO
_KILLINFO.fields_by_name['killer'].message_type = _PLAYERINFO
_KILLINFO.fields_by_name['grenade_position'].message_type = math_pb2._VECTOR
DESCRIPTOR.message_types_by_name['GameData'] = _GAMEDATA
DESCRIPTOR.message_types_by_name['PlayerPositions'] = _PLAYERPOSITIONS
DESCRIPTOR.message_types_by_name['VoteResult'] = _VOTERESULT
DESCRIPTOR.message_types_by_name['PlayerInfo'] = _PLAYERINFO
DESCRIPTOR.message_types_by_name['KillInfo'] = _KILLINFO
DESCRIPTOR.message_types_by_name['PlayerList'] = _PLAYERLIST
DESCRIPTOR.message_types_by_name['ServerReply'] = _SERVERREPLY

class GameData(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMEDATA
  
  # @@protoc_insertion_point(class_scope:da.protobuf.GameData)

class PlayerPositions(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYERPOSITIONS
  
  # @@protoc_insertion_point(class_scope:da.protobuf.PlayerPositions)

class VoteResult(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VOTERESULT
  
  # @@protoc_insertion_point(class_scope:da.protobuf.VoteResult)

class PlayerInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYERINFO
  
  # @@protoc_insertion_point(class_scope:da.protobuf.PlayerInfo)

class KillInfo(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _KILLINFO
  
  # @@protoc_insertion_point(class_scope:da.protobuf.KillInfo)

class PlayerList(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYERLIST
  
  # @@protoc_insertion_point(class_scope:da.protobuf.PlayerList)

class ServerReply(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SERVERREPLY
  
  # @@protoc_insertion_point(class_scope:da.protobuf.ServerReply)

# @@protoc_insertion_point(module_scope)
