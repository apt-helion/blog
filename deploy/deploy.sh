#!/bin/bash

git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

ssh apps@$IP -p $PORT <<EOF
  export PRODUCTION=true
  cd $DEPLOY_DIR
  source env/bin/activate
  pip install --upgrade -e git+https://github.com/yevrah/simplerr#egg=simplerr
  pip install --upgrade -e git+https://github.com/beanpuppy/python-markdown2#egg=python-markdown2
  ./manage.py updatedb
EOF
