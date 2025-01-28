# Protocol Buffers

This folder contains protocol buffer definitions for all the
services in the framework. All services interact among each other using
the APIs defined in this folder. Each service folder is structured in the following way:

```
proto/
├─ service1/
│  ├─ v1
│     ├─ service.proto
│     ├─ somefile.proto
│     ├─ ...
│  ├─ v2
│  ├─ ...
├─ service2/
│  ...
```

Each service `proto` definition is versioned and separated in its own version
folder. Versions are subject to change when the messages types change and
general breaking changes.
