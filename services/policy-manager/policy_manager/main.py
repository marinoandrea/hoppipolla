import logging
from concurrent import futures

import grpc
from policy_manager.grpc import PolicyManagerGRPCServicer
from policy_manager.protos import policy_pb2_grpc


def main():
    logging.basicConfig()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    policy_pb2_grpc.add_PolicyManagerServicer_to_server(
        PolicyManagerGRPCServicer(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
