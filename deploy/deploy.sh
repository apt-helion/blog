#!/bin/bash

ssh apps@$IP -p $PORT <<EOF
  export TERM=linux
  export TERMINFO=/etc/terminfo
  export PRODUCTION=true
  cd $DEPLOY_DIR
  git pull
  source env/bin/activate
  ./manage.py updatedb
EOF
