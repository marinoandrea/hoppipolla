<img src="assets/logotype.svg?raw=true" width="70%"  />

---

> [!WARNING]  
> This software is in early phase of development and is not ready for
> production environments.

Hoppipolla is a distributed framework for user-side responsible networking based
on the SCION Internet protocol. It implements part of the
[Responsible Internet proposal](https://link.springer.com/article/10.1007/s10922-020-09564-7)
with an approach inspired by the architecture designed in the [Accounting Value Effects for Responsible Networking
](https://doi.org/10.1145/3472951.3473507) paper and by the [User-driven Path verification and control for Inter-domain networks](https://upin-project.nl/) (UPIN) project.

Once installed, Hoppipolla allows the user to publish policies expressed in Answer Set Programming (ASP) to select network nodes (i.e., autonomous systems) that comply with them when routing packets to other remote addresses in the SCION network.

An example of such policy in natural language:

```
Do not route network traffic through nodes that are located in country X
```

Which, using the Hoppipolla-specific ASP syntax would look like:

```
valid(Path) :- country(Hop, "X"), hop(Hop), path(Path), contains(Path, Hop).
```

The framework is constituted by a suite of services and the language-specific
SDKs used to interact with them from the client side. All of the services expose
a gRPC API defined in the [`protos`](protos) folder that can be used directly in place of
the SDK of choice.

## Installation

> [!WARNING]
> TBD

## Documentation

> [!WARNING]
> TBD

## Examples

The following snippet shows a simple usage of the Python SDK:

```python
config = hp.HoppipollaClientConfig() # default values
client = hp.HoppipollaClient.from_config(config)

issuer = client.get_default_issuer()

policy1 = client.publish_policy(
    issuer,
    'valid(Path) :- country(Hop, "X"), hop(Hop), path(Path), contains(Path, Hop).'
)

result = client.ping("1-ff00:0:110,10.0.0.1")
```

## License

Hoppipolla is [GNU GPL v3.0 licensed](/blob/main/LICENSE).
