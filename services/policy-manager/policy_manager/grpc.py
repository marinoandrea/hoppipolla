import logging
from datetime import datetime

import grpc
from google.protobuf.empty_pb2 import Empty
from policy_manager.domain.entities import (Hop, Identifier, Issuer, Path,
                                            Policy, TimeInterval)
from policy_manager.domain.errors import InvalidInputError
from policy_manager.domain.use_cases import (CreatePolicyInput,
                                             UpdatePolicyInput,
                                             ValidatePathInput)
from policy_manager.protos.policy_pb2 import (CreatePolicyRequest,
                                              CreatePolicyResponse,
                                              DeletePolicyRequest,
                                              GetDefaultIssuerResponse,
                                              GetLatestPolicyTimestampResponse,
                                              GetPolicyResponse)
from policy_manager.protos.policy_pb2 import Issuer as IssuerPb
from policy_manager.protos.policy_pb2 import ListPoliciesResponse
from policy_manager.protos.policy_pb2 import Policy as PolicyPb
from policy_manager.protos.policy_pb2 import (UpdatePolicyRequest,
                                              UpdatePolicyResponse,
                                              ValidatePathRequest,
                                              ValidatePathResponse)
from policy_manager.protos.policy_pb2_grpc import PolicyManagerServicer
from policy_manager.service import PolicyManagerService


def map_issuer_to_message(issuer: Issuer):
    return IssuerPb(
        id=str(issuer.id),
        created_at=issuer.created_at.isoformat(timespec="milliseconds"),
        updated_at=issuer.updated_at.isoformat(timespec="milliseconds"),
        name=issuer.name,
        default=issuer.default,
        description=issuer.description
    )


def map_policy_to_message(policy: Policy):
    return PolicyPb(
        id=str(policy.id),
        created_at=policy.created_at.isoformat(timespec="milliseconds"),
        updated_at=policy.updated_at.isoformat(timespec="milliseconds"),
        active=policy.active,
        title=policy.title,
        description=policy.description,
        statements=policy.statements,
        issuer=map_issuer_to_message(policy.issuer)
    )


class PolicyManagerGRPCServicer(PolicyManagerServicer):
    """
    The gRPC service implementation for the policy manager. Every RPC is
    conceived as a unit-of-work and is self-contained and behaves statelessly
    across multiple call; persistance is ensured across database sessions.
    """

    def CreatePolicy(
        self,
        request: CreatePolicyRequest,
        context: grpc.ServicerContext
    ) -> CreatePolicyResponse | None:
        """
        This RPC handler represents the external API for adding a path-level
        policy to the service.
        """
        response = CreatePolicyResponse()

        input_data = CreatePolicyInput(
            issuer_id=Identifier(request.issuer_id),
            title=request.title,
            statements=request.statements,
            description=request.description
        )

        try:
            output = PolicyManagerService.execute_create_policy(input_data)
            response = CreatePolicyResponse(policy=map_policy_to_message(output.policy))

        except InvalidInputError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            logging.debug(e)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def UpdatePolicy(
        self,
        request: UpdatePolicyRequest,
        context: grpc.ServicerContext
    ) -> UpdatePolicyResponse | None:
        """
        This RPC handler represents the external API for updating a path-level
        policy to the service.
        """
        response = UpdatePolicyResponse()

        input_data = UpdatePolicyInput(
            id=Identifier(request.id),
            title=request.title,
            statements=request.statements,
            description=request.description
        )

        try:
            output = PolicyManagerService.execute_update_policy(input_data)
            response = UpdatePolicyResponse(policy=map_policy_to_message(output.policy))

        except InvalidInputError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            logging.debug(e)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def ListPolicies(self, _, context):
        response = ListPoliciesResponse()

        try:
            output = PolicyManagerService.execute_list_all_policies()
            response = ListPoliciesResponse(policies=list(map(map_policy_to_message, output)))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def GetDefaultIssuer(self, _, context: grpc.ServicerContext):
        response = GetDefaultIssuerResponse()

        try:
            output = PolicyManagerService.execute_get_default_issuer()
            response = GetDefaultIssuerResponse(issuer=map_issuer_to_message(output))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def ValidatePath(
        self,
        request: ValidatePathRequest,
        context: grpc.ServicerContext
    ) -> ValidatePathResponse | None:
        """
        This RPC handler represents the external API for validating a path.
        """
        response = ValidatePathResponse()

        path = Path(
            fingerprint=request.path.fingerprint,
            isd_as_dst=request.path.dst_isd_as,
            isd_as_src=request.path.src_isd_as,
            hops=[Hop(
                isd_as=hop.isd_as,
                inbound_interface=hop.inbound_interface,
                outbound_interface=hop.outbound_interface
            ) for hop in request.path.hops]
        )

        if request.start_time and request.end_time:
            input_data = ValidatePathInput(
                path=path,
                interval=TimeInterval(
                    datetime_start=datetime.fromisoformat(request.start_time),
                    datetime_end=datetime.fromisoformat(request.end_time)
                )
            )
        else:
            input_data = ValidatePathInput(path=path)

        try:
            output = PolicyManagerService.execute_validate_path(input_data)
            response = ValidatePathResponse(
                fingerprint=request.path.fingerprint,
                valid=output.valid
            )

        except InvalidInputError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            logging.debug(e)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def GetLatestPolicyTimestamp(self, _, context) -> GetLatestPolicyTimestampResponse | None:
        response = GetLatestPolicyTimestampResponse()

        try:
            output = PolicyManagerService.execute_get_latest_policy_timestamp()
            response = GetLatestPolicyTimestampResponse(
                timestamp=output
                .astimezone()
                .isoformat(timespec="milliseconds")
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def GetPolicy(self, req, context):
        response = GetPolicyResponse()

        try:
            output = PolicyManagerService.execute_get_policy(req.id)
            if output is not None:
                response = GetPolicyResponse(policy=map_policy_to_message(output))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def DeletePolicy(self, req: DeletePolicyRequest, context):
        response = Empty()

        try:
            PolicyManagerService.execute_delete_policy(Identifier(req.id))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response
