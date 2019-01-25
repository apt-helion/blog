#!/bin/bash

echo "Pushing Git"
git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

echo "SSH"
ssh apps@$IP -p $PORT <<EOF
  export PRODUCTION=true
  cd $DEPLOY_DIR
  source env/bin/activate
  ./bin/updatedb.py
EOF
