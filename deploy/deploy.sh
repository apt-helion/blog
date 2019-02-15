#!/bin/bash

git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

ssh apps@$IP -p $PORT <<EOF
  export PRODUCTION=true
  cd $DEPLOY_DIR

  python3.6 -m venv env_tmp
  source env_tmp/bin/activate
  pip install -r requirements.txt

  deactivate
  rm -rf env/
  mv env_tmp env
  source env/bin/activate

  ./manage.py updatedb
EOF
