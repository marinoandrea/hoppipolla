FROM golang:1.23.4-alpine AS builder

WORKDIR /build

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-w -s" -o main

FROM scratch AS runner

WORKDIR /app

COPY --from=builder /build/main /app/main

ENTRYPOINT ["/app/main"]