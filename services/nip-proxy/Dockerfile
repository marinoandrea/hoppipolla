FROM node:lts-slim as base

RUN apt-get -qy update && apt-get -qy install openssl

###

FROM base as builder

WORKDIR /build

COPY package.json package-lock.json tsconfig.json ./

RUN npm ci

COPY eslint.config.mjs ./
COPY src ./src

RUN npm run build


###

FROM base AS runtime

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --omit dev

COPY --from=builder /build/dist ./dist

CMD [ "node", "dist/src/index.js" ]

