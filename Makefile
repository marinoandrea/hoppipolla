.PHONY: proto

proto:
	rm -rf ./pkg/proto/*
	protoc -I ./proto \
		--go_out=./pkg/proto \
		--go_opt=paths=source_relative \
		--go-grpc_out=./pkg/proto \
		--go-grpc_opt=paths=source_relative \
		--experimental_allow_proto3_optional \
		path_analyzer/v1/service.proto \
		policy_manager/v1/service.proto \
		nip_proxy/v1/service.proto \
