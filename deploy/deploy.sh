#!/bin/bash

git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

ssh apps@$IP -p $PORT <<EOF
  export PRODUCTION=true
  cd $DEPLOY_DIR
  rm -rf env/
  python3.6 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  ./manage.py updatedb
EOF
