#!/usr/bin/env bash
set -e
# aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/a9w6z7w5
# gcloud auth configure-docker
docker build -t skypilot-tutorial:latest .
docker tag skypilot-tutorial:latest gcr.io/skycamp-skypilot-fastchat/skypilot-tutorial:latest
docker push  gcr.io/skycamp-skypilot-fastchat/skycamp-skypilot-fastchat/skypilot-tutorial:latest
