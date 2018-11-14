#!/bin/bash

echo "hi"
git config --global push.default matching
echo "hi"
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
echo "hi"
git push deploy master
echo "hi"

ssh apps@$IP -p $PORT <<EOF
  cd $DEPLOY_DIR
EOF
