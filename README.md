# blog
Blog source code 

[![Build Status](https://travis-ci.com/apt-helion/blog.svg?branch=master)](https://travis-ci.com/apt-helion/blog)

## Setting up on a development environment 
```
# Clone it
git clone https://github.com/apt-helion/blog
cd blog

# Using the python virtual environment module (venv), create a python
# environment into "./env"
python3.6 -m venv env

# Setup your shell for this project
source env/bin/activate

# Install requirements for this project
pip install -r requirements.txt

# Set environment variable (optional)
export DEVBOX=GENERIC_DEV_MACHINE

# Copy example_config.py to config.py then edit it
cp website/example_config.py config.py
vim website/config.py

# Now you should source 'website/blog.sql' into your database

# Start the server
./manage.py runserver
```

You should be able to view it on `127.0.0.1:5000`.

If you want you can set up your `/etc/hosts` to give it a hostname e.g:
```
# /etc/hosts

# address           hostname

127.0.0.1:5000      dev.blog
```
Now you can access it through `dev.blog`.
