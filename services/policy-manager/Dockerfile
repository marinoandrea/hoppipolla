FROM rust:slim-bullseye AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y cmake gcc g++ protobuf-compiler

COPY ./proto ./proto
COPY ./services/policy-manager ./services/policy-manager

RUN cargo build --release \
    --manifest-path ./services/policy-manager/Cargo.toml \
    --target-dir ./target

###

FROM debian:stable-slim AS runner

WORKDIR /app

COPY --from=builder /build/target/release/policy-manager /app/policy-manager

ENTRYPOINT [ "/app/policy-manager" ]