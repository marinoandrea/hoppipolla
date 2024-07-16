#!/bin/sh

GENERATED_PATH=./src/protos

npx grpc_tools_node_protoc \
    -I../../protos \
    --ts_out=grpc_js:$GENERATED_PATH \
    --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
    ../../protos/path.proto \
    ../../protos/policy.proto \
    ../../protos/common.proto


add_line_to_file() {
  local FILE=$1
  local TEMP_FILE=$(mktemp)
  echo "// @ts-nocheck" | cat - "$FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$FILE"
  echo "Generated $FILE"
}

export -f add_line_to_file
find "$GENERATED_PATH" -type f -exec bash -c 'add_line_to_file "$0"' {} \;
