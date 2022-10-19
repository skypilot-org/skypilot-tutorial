#!/usr/bin/env bash
set -e
# aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/a9w6z7w5
docker build -t skypilot-tutorial:latest .
docker tag skypilot-tutorial:latest public.ecr.aws/a9w6z7w5/skypilot-tutorial:latest
docker push public.ecr.aws/a9w6z7w5/skypilot-tutorial:latest
