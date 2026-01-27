#!/usr/bin/env sh

construct=$1
if [ -z ${construct// } ]; then
    echo missing construct name
    exit 1
fi

template=cdk.out/$construct.template.json
if [ ! -f $template ]; then
    echo template not found
    exit 1
fi

cdk synth -q && uvx --from aws-sam-cli sam build -t $template || exit
uvx --from aws-sam-cli sam local start-api -t $template -p 8000 --warm-containers eager
