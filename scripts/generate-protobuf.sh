#!/bin/bash

base_dir="services"

for subfolder in "$base_dir"/*/; do
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

echo "Completed."
