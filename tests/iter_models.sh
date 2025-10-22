#!/bin/bash

# Usage: iter_models.sh <testsuite.sh> [llme args...]

. "$(dirname "$0")/utils.sh"

testsuite=$1
shift

url=`$LLME "$@" --dump-config | jq -r '.base_url'`
echo "url: $url"

models=`curl -s "$url/models" | jq '.. | .id? | select(. != null)' -r`
models=`echo $models`

echo "models: $models"
for model in $models; do
    echo "Model: $model - Test suite: $testsuite"
    "$testsuite" "$@" -m "$model"
done 
