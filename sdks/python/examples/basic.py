import hoppipolla as hp

POLICY_1 = """
#const min_sustainability_index = 10.

-valid(Path) :- Idx < min_sustainability_index,
    sustainability_index(Data, Idx),
    latest_data(Hop, Data),
    contains(Path, Hop).
"""

POLICY_2 = """
-valid(Path) :- location(Hop, "RS"), contains(Path, Hop).
"""


def main():
    config = hp.HoppipollaClientConfig()
    client = hp.HoppipollaClient.from_config(config)

    issuer = client.get_default_issuer()

    policy1 = client.publish_policy(issuer, POLICY_1)
    policy2 = client.publish_policy(issuer, POLICY_2)

    result = client.ping("1-ff00:0:110,10.0.0.1")

    print(result)

    client.delete_policy(policy2.id)

    result = client.ping("1-ff00:0:110,10.0.0.1")

    print(result)


if __name__ == '__main__':
    main()
