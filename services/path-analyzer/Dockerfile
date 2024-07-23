FROM node:lts-slim as base-node

RUN apt-get -qy update && apt-get -qy install openssl

###

FROM golang:1.21-bookworm as base-scion

RUN apt-get -qy update && apt-get -qy install git

WORKDIR /scion

RUN git clone https://github.com/scionproto/scion; \
    cd scion; \
    go build -o bin/ ./...

###

FROM base-node as builder

WORKDIR /build

COPY package.json package-lock.json tsconfig.json ./

RUN npm ci

COPY eslint.config.mjs ./
COPY src ./src

RUN npm run build


###

FROM base-node AS runtime

WORKDIR /app

COPY --from=base-scion /scion /

ENV SCION_EXE_PATH ./scion/bin/scion

COPY package.json package-lock.json ./

RUN npm ci --omit dev

COPY --from=builder /build/dist ./dist

CMD [ "node", "dist/src/index.js" ]

