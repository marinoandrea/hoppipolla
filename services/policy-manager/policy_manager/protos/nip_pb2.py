# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nip.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tnip.proto\x12\x0ehoppipolla.nip\"\xf7\x02\n\rEnergyReading\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06isd_as\x18\x02 \x01(\t\x12\x12\n\nmachine_id\x18\x03 \x01(\t\x12\x14\n\x0c\x63ollected_at\x18\x04 \x01(\t\x12\x1e\n\x16\x65nergy_consumption_kWh\x18\x05 \x01(\x02\x12\x1c\n\x14\x63pu_usage_percentage\x18\x06 \x01(\x02\x12\x1f\n\x17memory_usage_percentage\x18\x07 \x01(\x02\x12\x1a\n\x12network_traffic_MB\x18\x08 \x01(\x02\x12\x1b\n\x13temperature_celsius\x18\t \x01(\x02\x12\x14\n\x0cpower_source\x18\n \x01(\t\x12\x0e\n\x06status\x18\x0b \x01(\t\x12\x1b\n\x13\x63\x61rbon_emissions_kg\x18\x0c \x01(\x02\x12#\n\x1brenewable_energy_percentage\x18\r \x01(\x02\x12 \n\x18\x65nergy_efficiency_rating\x18\x0e \x01(\t\"_\n\nGeoReading\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06isd_as\x18\x02 \x01(\t\x12\x14\n\x0c\x63ollected_at\x18\x03 \x01(\t\x12\x1f\n\x17operating_country_codes\x18\x04 \x03(\t\"P\n\x18GetEnergyReadingsRequest\x12\x0e\n\x06isd_as\x18\x01 \x01(\t\x12\x12\n\nstart_time\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_time\x18\x03 \x01(\t\"H\n\x19GetEnergyReadingsResponse\x12+\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1d.hoppipolla.nip.EnergyReading\"M\n\x15GetGeoReadingsRequest\x12\x0e\n\x06isd_as\x18\x01 \x01(\t\x12\x12\n\nstart_time\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_time\x18\x03 \x01(\t\"B\n\x16GetGeoReadingsResponse\x12(\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1a.hoppipolla.nip.GeoReading2\xd9\x01\n\x08NipProxy\x12j\n\x11GetEnergyReadings\x12(.hoppipolla.nip.GetEnergyReadingsRequest\x1a).hoppipolla.nip.GetEnergyReadingsResponse\"\x00\x12\x61\n\x0eGetGeoReadings\x12%.hoppipolla.nip.GetGeoReadingsRequest\x1a&.hoppipolla.nip.GetGeoReadingsResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nip_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ENERGYREADING']._serialized_start=30
  _globals['_ENERGYREADING']._serialized_end=405
  _globals['_GEOREADING']._serialized_start=407
  _globals['_GEOREADING']._serialized_end=502
  _globals['_GETENERGYREADINGSREQUEST']._serialized_start=504
  _globals['_GETENERGYREADINGSREQUEST']._serialized_end=584
  _globals['_GETENERGYREADINGSRESPONSE']._serialized_start=586
  _globals['_GETENERGYREADINGSRESPONSE']._serialized_end=658
  _globals['_GETGEOREADINGSREQUEST']._serialized_start=660
  _globals['_GETGEOREADINGSREQUEST']._serialized_end=737
  _globals['_GETGEOREADINGSRESPONSE']._serialized_start=739
  _globals['_GETGEOREADINGSRESPONSE']._serialized_end=805
  _globals['_NIPPROXY']._serialized_start=808
  _globals['_NIPPROXY']._serialized_end=1025
# @@protoc_insertion_point(module_scope)
