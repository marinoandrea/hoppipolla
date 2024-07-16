FROM node:lts-slim as base

RUN apt-get -qy update && apt-get -qy install openssl

###

FROM base as builder

WORKDIR /build

COPY package.json package-lock.json ./

RUN npm ci
RUN npm run build

###

FROM base AS runtime

WORKDIR /app

COPY . .

RUN npm ci --omit dev

COPY --from=builder /build/dist ./dist

CMD [ "node", "dist/index.js" ]

