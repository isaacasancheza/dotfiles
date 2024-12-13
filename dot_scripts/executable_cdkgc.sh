#!/usr/bin/env sh

REGION=$(aws configure get region --output text)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

pnpx aws-cdk gc aws://$ACCOUNT_ID/$REGION --unstable gc --confirm true

