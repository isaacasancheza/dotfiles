#!/usr/bin/env sh

functionName=$1

if [ ! $functionName ]; then
    echo missing function name
    exit 1
fi

if [ ! -d cdk.out ]; then
    echo template not found
    exit 1
fi

template=$(find cdk.out -type f -name '*.template.json')

if [ -z $template ]; then
    echo template not found
    exit 1
fi

cdk synth && sam build -t $template || exit
sam local invoke -t $template $functionName
