from importlib.machinery import SourceFileLoader

from dotenv import load_dotenv

import hoppipolla as hp

load_dotenv()

loader = SourceFileLoader("runtime", "../utils/runtime.py")
runtime = loader.load_module()


def main():
    with open("policies/main.lp", "r") as f:
        policy = f.read()

    config = hp.HoppipollaClientConfig()
    config.sciond.base_url = runtime.get_sciond_base_url("111")

    client = hp.HoppipollaClient.from_config(config)

    result = client.ping("1-ff00:0:113,127.0.0.1")

    if not result.success:
        exit(1)

    issuer = client.get_default_issuer()

    client.publish_policy(issuer, policy)

    result = client.ping("1-ff00:0:113,127.0.0.1")

    if result.success:
        exit(1)

    exit(0)


if __name__ == '__main__':
    main()
