import logging
from typing import Generator

import grpc
from policy_manager.domain.entities import Hop, Identifier, Path, TimeInterval
from policy_manager.domain.errors import InvalidInputError
from policy_manager.domain.use_cases import (CreatePolicyInput,
                                             ValidatePathInput)
from policy_manager.protos.policy_pb2 import (CreatePolicyRequest,
                                              CreatePolicyResponse,
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
    ) -> Generator[CreatePolicyResponse, None, None]:
        """
        This RPC handler represents the external API for adding a path-level
        policy to the service.
        """
        input_data = CreatePolicyInput(
            issuer_id=Identifier(request.issuer_id),
            statements=request.statements,
            description=request.description
        )

        try:
            output = PolicyManagerService.execute_create_policy(input_data)
            yield CreatePolicyResponse(id=str(output.policy.id))

        except InvalidInputError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

    def DeletePolicy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListPolicies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidatePath(
        self,
        request: ValidatePathRequest,
        context: grpc.ServicerContext
    ) -> Generator[ValidatePathResponse, None, None]:
        """
        This RPC handler represents the external API for validating a path.
        """
        input_data = ValidatePathInput(
            path=Path(
                fingerprint=request.path.fingerprint,
                isd_as_dst=request.path.dst_isd_as,
                isd_as_src=request.path.src_isd_as,
                hops=[Hop(isd_as=hop.isd_as, ifid=hop.ifid)
                      for hop in request.path.hops]
            ),
            interval=TimeInterval(
                request.data_interval.start_time.ToDatetime(),
                request.data_interval.end_time.ToDatetime(),
            )
        )
        try:
            output = PolicyManagerService.execute_validate_path(input_data)
            yield ValidatePathResponse(
                fingerprint=request.path.fingerprint,
                valid=output.valid
            )

        except InvalidInputError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            logging.error(str(e))

    def GetLatestPolicyTimestamp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
