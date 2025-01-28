# Network Information Plane (NIP) Proxy Service

This service represents a central gateway to access network metadata from
different sources. The data model is standardized and is dependent on the types
supported by the [`Policy Manager`](/services/policy-manager/) service, namely:
categorical (i.e., `string`), integer (i.e., `i32`), and boolean.

The service returns two types of data given a request containing a topology (a
graph with the relevant links) and optional source and destination nodes for
path search.
