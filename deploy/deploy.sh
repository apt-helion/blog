#!/bin/bash

echo "Pushing Git"
git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

echo "SSHing"
ssh apps@$IP -p $PORT <<EOF
  cd $DEPLOY_DIR
EOF
