# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import policy_pb2 as policy__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in policy_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class PolicyManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePolicy = channel.unary_unary(
                '/hoppipolla.policy.PolicyManager/CreatePolicy',
                request_serializer=policy__pb2.CreatePolicyRequest.SerializeToString,
                response_deserializer=policy__pb2.CreatePolicyResponse.FromString,
                _registered_method=True)
        self.DeletePolicy = channel.unary_unary(
                '/hoppipolla.policy.PolicyManager/DeletePolicy',
                request_serializer=policy__pb2.DeletePolicyRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.CreateIssuer = channel.unary_unary(
                '/hoppipolla.policy.PolicyManager/CreateIssuer',
                request_serializer=policy__pb2.CreateIssuerRequest.SerializeToString,
                response_deserializer=policy__pb2.CreateIssuerResponse.FromString,
                _registered_method=True)
        self.ListPolicies = channel.unary_unary(
                '/hoppipolla.policy.PolicyManager/ListPolicies',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=policy__pb2.ListPoliciesRespose.FromString,
                _registered_method=True)
        self.ValidatePath = channel.unary_unary(
                '/hoppipolla.policy.PolicyManager/ValidatePath',
                request_serializer=policy__pb2.ValidatePathRequest.SerializeToString,
                response_deserializer=policy__pb2.ValidatePathResponse.FromString,
                _registered_method=True)
        self.GetLatestPolicyTimestamp = channel.unary_unary(
                '/hoppipolla.policy.PolicyManager/GetLatestPolicyTimestamp',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=policy__pb2.GetLatestPolicyTimestampResponse.FromString,
                _registered_method=True)


class PolicyManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreatePolicy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePolicy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateIssuer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListPolicies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidatePath(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestPolicyTimestamp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PolicyManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreatePolicy': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePolicy,
                    request_deserializer=policy__pb2.CreatePolicyRequest.FromString,
                    response_serializer=policy__pb2.CreatePolicyResponse.SerializeToString,
            ),
            'DeletePolicy': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePolicy,
                    request_deserializer=policy__pb2.DeletePolicyRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'CreateIssuer': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateIssuer,
                    request_deserializer=policy__pb2.CreateIssuerRequest.FromString,
                    response_serializer=policy__pb2.CreateIssuerResponse.SerializeToString,
            ),
            'ListPolicies': grpc.unary_unary_rpc_method_handler(
                    servicer.ListPolicies,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=policy__pb2.ListPoliciesRespose.SerializeToString,
            ),
            'ValidatePath': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidatePath,
                    request_deserializer=policy__pb2.ValidatePathRequest.FromString,
                    response_serializer=policy__pb2.ValidatePathResponse.SerializeToString,
            ),
            'GetLatestPolicyTimestamp': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLatestPolicyTimestamp,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=policy__pb2.GetLatestPolicyTimestampResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hoppipolla.policy.PolicyManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('hoppipolla.policy.PolicyManager', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PolicyManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreatePolicy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hoppipolla.policy.PolicyManager/CreatePolicy',
            policy__pb2.CreatePolicyRequest.SerializeToString,
            policy__pb2.CreatePolicyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeletePolicy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hoppipolla.policy.PolicyManager/DeletePolicy',
            policy__pb2.DeletePolicyRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateIssuer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hoppipolla.policy.PolicyManager/CreateIssuer',
            policy__pb2.CreateIssuerRequest.SerializeToString,
            policy__pb2.CreateIssuerResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListPolicies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hoppipolla.policy.PolicyManager/ListPolicies',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            policy__pb2.ListPoliciesRespose.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ValidatePath(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hoppipolla.policy.PolicyManager/ValidatePath',
            policy__pb2.ValidatePathRequest.SerializeToString,
            policy__pb2.ValidatePathResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetLatestPolicyTimestamp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/hoppipolla.policy.PolicyManager/GetLatestPolicyTimestamp',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            policy__pb2.GetLatestPolicyTimestampResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
