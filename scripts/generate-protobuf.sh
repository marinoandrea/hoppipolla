#!/bin/bash

generate_protobufs(){
  for subfolder in "$1"/*/; do
    if [ -d "$subfolder" ]; then
      echo "Generating protobuf bindings for: $subfolder"

      cd "$subfolder" || continue

      if [ -f "scripts/generate-protobuf.sh" ]; then
        ./scripts/generate-protobuf.sh
      else
        echo "No generate-protobuf.sh script found in $subfolder"
      fi

      cd "../.."
    fi
  done
}

generate_protobufs services
generate_protobufs sdks
generate_protobufs apps

echo "Completed."
