# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: policy.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import path_pb2 as path__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cpolicy.proto\x12\x11hoppipolla.policy\x1a\x1bgoogle/protobuf/empty.proto\x1a\npath.proto\"L\n\x06Issuer\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_description\"u\n\x06Policy\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tissuer_id\x18\x02 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x03 \x01(\x08\x12\x12\n\nstatements\x18\x04 \x01(\t\x12\x18\n\x0b\x64\x65scription\x18\x05 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_description\"f\n\x13\x43reatePolicyRequest\x12\x11\n\tissuer_id\x18\x01 \x01(\t\x12\x12\n\nstatements\x18\x02 \x01(\t\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_description\"\"\n\x14\x43reatePolicyResponse\x12\n\n\x02id\x18\x01 \x01(\t\"!\n\x13\x44\x65letePolicyRequest\x12\n\n\x02id\x18\x01 \x01(\t\"#\n\x13\x43reateIssuerRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\"\n\x14\x43reateIssuerResponse\x12\n\n\x02id\x18\x01 \x01(\t\"C\n\x14ListPoliciesResponse\x12+\n\x08policies\x18\x01 \x03(\x0b\x32\x19.hoppipolla.policy.Policy\"`\n\x13ValidatePathRequest\x12#\n\x04path\x18\x01 \x01(\x0b\x32\x15.hoppipolla.path.Path\x12\x12\n\nstart_time\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_time\x18\x03 \x01(\t\":\n\x14ValidatePathResponse\x12\x13\n\x0b\x66ingerprint\x18\x01 \x01(\t\x12\r\n\x05valid\x18\x02 \x01(\x08\"5\n GetLatestPolicyTimestampResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\"^\n\x18GetDefaultIssuerResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_description2\xa3\x05\n\rPolicyManager\x12\x61\n\x0c\x43reatePolicy\x12&.hoppipolla.policy.CreatePolicyRequest\x1a\'.hoppipolla.policy.CreatePolicyResponse\"\x00\x12P\n\x0c\x44\x65letePolicy\x12&.hoppipolla.policy.DeletePolicyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x61\n\x0c\x43reateIssuer\x12&.hoppipolla.policy.CreateIssuerRequest\x1a\'.hoppipolla.policy.CreateIssuerResponse\"\x00\x12Q\n\x0cListPolicies\x12\x16.google.protobuf.Empty\x1a\'.hoppipolla.policy.ListPoliciesResponse\"\x00\x12\x61\n\x0cValidatePath\x12&.hoppipolla.policy.ValidatePathRequest\x1a\'.hoppipolla.policy.ValidatePathResponse\"\x00\x12i\n\x18GetLatestPolicyTimestamp\x12\x16.google.protobuf.Empty\x1a\x33.hoppipolla.policy.GetLatestPolicyTimestampResponse\"\x00\x12Y\n\x10GetDefaultIssuer\x12\x16.google.protobuf.Empty\x1a+.hoppipolla.policy.GetDefaultIssuerResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'policy_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ISSUER']._serialized_start=76
  _globals['_ISSUER']._serialized_end=152
  _globals['_POLICY']._serialized_start=154
  _globals['_POLICY']._serialized_end=271
  _globals['_CREATEPOLICYREQUEST']._serialized_start=273
  _globals['_CREATEPOLICYREQUEST']._serialized_end=375
  _globals['_CREATEPOLICYRESPONSE']._serialized_start=377
  _globals['_CREATEPOLICYRESPONSE']._serialized_end=411
  _globals['_DELETEPOLICYREQUEST']._serialized_start=413
  _globals['_DELETEPOLICYREQUEST']._serialized_end=446
  _globals['_CREATEISSUERREQUEST']._serialized_start=448
  _globals['_CREATEISSUERREQUEST']._serialized_end=483
  _globals['_CREATEISSUERRESPONSE']._serialized_start=485
  _globals['_CREATEISSUERRESPONSE']._serialized_end=519
  _globals['_LISTPOLICIESRESPONSE']._serialized_start=521
  _globals['_LISTPOLICIESRESPONSE']._serialized_end=588
  _globals['_VALIDATEPATHREQUEST']._serialized_start=590
  _globals['_VALIDATEPATHREQUEST']._serialized_end=686
  _globals['_VALIDATEPATHRESPONSE']._serialized_start=688
  _globals['_VALIDATEPATHRESPONSE']._serialized_end=746
  _globals['_GETLATESTPOLICYTIMESTAMPRESPONSE']._serialized_start=748
  _globals['_GETLATESTPOLICYTIMESTAMPRESPONSE']._serialized_end=801
  _globals['_GETDEFAULTISSUERRESPONSE']._serialized_start=803
  _globals['_GETDEFAULTISSUERRESPONSE']._serialized_end=897
  _globals['_POLICYMANAGER']._serialized_start=900
  _globals['_POLICYMANAGER']._serialized_end=1575
# @@protoc_insertion_point(module_scope)
