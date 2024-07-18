<img src="assets/logotype.svg?raw=true" width="60%"  />

---

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![CI](https://github.com/marinoandrea/hoppipolla/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)
[![codecov](https://codecov.io/github/marinoandrea/hoppipolla/graph/badge.svg?token=X0T25B3TQP)](https://codecov.io/github/marinoandrea/hoppipolla)

> [!WARNING]  
> This software is in early phase of development and is not ready for
> production environments.

Hoppipolla (Icelandic for _"hopping into puddles"_) is a distributed framework
for user-side responsible networking based on the SCION Internet protocol. It implements
part of the [Responsible Internet proposal](https://link.springer.com/article/10.1007/s10922-020-09564-7)
with an approach inspired by the architecture designed in the [Accounting Value Effects for Responsible Networking
](https://doi.org/10.1145/3472951.3473507) paper and by the [User-driven Path verification and control for Inter-domain networks](https://upin-project.nl/) (UPIN) project.

Once installed, Hoppipolla allows the user to publish policies expressed in
Answer Set Programming (ASP) to select network nodes (i.e., autonomous systems)
that comply with them when routing packets to other remote addresses in the
SCION network.

An example of such policy in natural language:

```
Do not route network traffic through nodes that are located in country X
```

Which, using the Hoppipolla-specific ASP syntax would look like:

```
-valid(Path) :- country(Hop, "X"), hop(Hop), path(Path), contains(Path, Hop).
```

The framework is constituted by a suite of services and the language-specific
SDKs used to interact with them from the client side. All of the services expose
a gRPC API defined in the [`protos`](protos) folder that can be used directly in place of
the SDK of choice.

## Installation

### Dependencies

In terms of external dependencies, Hoppipolla depends exclusively on SCION. The
user is expected to provide an entrypoint to the SCION stack via a stable
connection to the SCION daemon.

Follow [this guide](https://docs.scionlab.org/content/install/) to install
SCION and use it within the SCIONLab testbed.

### Docker Compose

At this stage, Hoppipolla is not ready for production in a fully distributed
environment. Therefore, for experimental work, it is recommendend that you run
it locally using `docker compose`.

You can find an example of the configuration options that can be passed to the
services in the [`.env.example`](.env.example) file.

> [!IMPORTANT]
> Most notably, the `HOPPIPOLLA_SCIOND_URI` env variable should be set to
> the address of the SCION daemon (e.g., 127.0.0.1:30255).

The repository contains a [`docker-compose.yml`](docker-compose.yml) file which
runs all the necessary services. You can sping up Hoppipolla on your machine
simply by running:

```
docker compose up
```

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
    '-valid(Path) :- country(Hop, "X"), hop(Hop), path(Path), contains(Path, Hop).'
)

result = client.ping("1-ff00:0:110,10.0.0.1")
```

## License

Hoppipolla is [GNU GPL v3.0 licensed](/blob/main/LICENSE).
