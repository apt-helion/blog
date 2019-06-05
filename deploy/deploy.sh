#!/bin/bash

git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

ssh apps@$IP -p $PORT <<EOF
  export TERM=linux
  export TERMINFO=/etc/terminfo
  export PRODUCTION=true
  cd $DEPLOY_DIR
  source env/bin/activate
  ./manage.py updatedb
EOF
