import logging
from datetime import datetime

import grpc
from policy_manager.domain.entities import Hop, Identifier, Path, TimeInterval
from policy_manager.domain.errors import InvalidInputError
from policy_manager.domain.use_cases import (CreatePolicyInput,
                                             ValidatePathInput)
from policy_manager.protos.policy_pb2 import (CreatePolicyRequest,
                                              CreatePolicyResponse,
                                              GetDefaultIssuerResponse,
                                              GetLatestPolicyTimestampResponse,
                                              ListPoliciesResponse, Policy,
                                              ValidatePathRequest,
                                              ValidatePathResponse)
from policy_manager.protos.policy_pb2_grpc import PolicyManagerServicer
from policy_manager.service import PolicyManagerService


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
            statements=request.statements,
            description=request.description
        )

        try:
            output = PolicyManagerService.execute_create_policy(input_data)
            response = CreatePolicyResponse(id=str(output.policy.id))

        except InvalidInputError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            logging.debug(e)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def DeletePolicy(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListPolicies(self, _, context):
        response = ListPoliciesResponse()

        try:
            output = PolicyManagerService.execute_list_all_policies()
            response = ListPoliciesResponse(policies=list(map(lambda p: Policy(
                id=str(p.id),
                active=p.active,
                description=p.description,
                statements=p.statements,
                issuer_id=str(p.issuer.id)
            ), output)))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

        return response

    def GetDefaultIssuer(self, _, context: grpc.ServicerContext):
        response = GetDefaultIssuerResponse()

        try:
            output = PolicyManagerService.execute_get_default_issuer()

            response = GetDefaultIssuerResponse(
                id=str(output.id),
                name=output.name,
                description=output.description
            )

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
