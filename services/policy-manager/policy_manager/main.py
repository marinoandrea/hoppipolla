import logging
import sys
from concurrent import futures
from datetime import datetime

import grpc
from policy_manager import before_startup_time
from policy_manager.config import config
from policy_manager.grpc import PolicyManagerGRPCServicer
from policy_manager.protos import policy_pb2_grpc


def main():
    logging.basicConfig(
        level=config.log_level,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    pool = futures.ThreadPoolExecutor(max_workers=config.n_workers)
    server = grpc.server(pool)

    policy_pb2_grpc.add_PolicyManagerServicer_to_server(
        PolicyManagerGRPCServicer(),
        server
    )

    address = f"{config.host}:{config.port}"
    server.add_insecure_port(address)
    server.start()

    after_startup_time = datetime.now()
    startup_duration_ms = (after_startup_time - before_startup_time).total_seconds() * 1000

    logging.info("service | running")
    logging.info(f"python  | {sys.version.split(" ")[0]}")
    logging.info(f"env     | {config.env}")
    logging.info(f"address | {address}")
    logging.info(f"startup | {startup_duration_ms}ms")

    server.wait_for_termination()


if __name__ == "__main__":
    main()
