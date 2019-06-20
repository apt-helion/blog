---
title: A Basic Deployment Guide For Aiohttp + Gunicorn + Nginx
category: development
date: 2018-07-04
thumbnail: aiohttp-deployment-thumb.png
tags: aiohttp,gunicorn,nginx,python
description:
---

In this guide we will be setting up a basic aiohttp app using Gunicorn and Nginx because the documentation on this I feel is very poor, as it took me a good few hours to figure out. Or maybe it was because I haven't used any of these technologies before... Either way, I didn't understand the documentation so I'm writing my own.

This guide assumes you are using Python3 and a Linux operating system with Systemd as the init system (e.g Ubuntu, CentOS, ...).

#### Table of Contents

* [Python Venv](#0x100-python-venv)
* [Aiohttp](#0x200-aiohttp)
* [Systemd Unit](#0x300-systemd-unti)
* [Nginx Conf](#0x400-nginx-conf)

### 0x100: Python Venv

The first thing everyone should always do everywhere no matter where they are, or who they with, or where they come from, or where they are going, is set up a virtual environment for Python. If you're app doesn't use a virtual environment, you're an idiot and you should create one ***RIGHT NOW.*** Here's how:

Use the python module `venv` to create a virtual environment called env (or anything else you prefer).

    [user@okcomputer]$ python -m venv env

And that's how you create a Python virtual environment. Now we want to install the `aiohttp` and `gunicorn` modules.

Source the environment:

    [user@okcomputer]$ source env/bin/activate

Install the modules:

    (env) [user@okcomputer]$ pip install aiohttp gunicorn

That's all we need to get started for now. You can install any other libraries you want into the environment with pip.

### 0x200: Aiohttp and Gunicorn

With our new Python environment we are ready to create an aiohttp app! If you don't know, aiohttp is an asynchronous HTTP server/client. It's very useful when you're creating a web crawler that uses asyncio, but when you attempt to call it through a normal web framework, it doesn't work because as it turns out every good framework in existence is a blocking program so nothing works. So then you look for a framework that supports asycnio, then you find aiohttp and you're like *'yeah this seems easy to use'*. But **NOPE**, it turns out the documentation sucks, and the documentation that is there is for a completely different technology stack so you have no idea what to do because you only know Apache and neither aiohttp nor Gunicorn have documentation for it. So then your like ***FUCK IT.*** I'll just buy another web sever, learn Nginx and put my crawler there'. So when you've finished setting it up and it works all nice and good, you've realised that it took way longer than it should have and so you write a blog post to rant about it because you don't like feeling as though it was wasted time.

For this guide are writing a simple aiohttp application which we will call `myapp.py`.

```python
from aiohttp import web async

def index(request):
    return web.Response(text="I work!")

async def factory():
    app = web.Application()
    app.router.add_get('/', index)
    return app
```

This is all we need to create a page that displays I work!. `factory` is our coroutine that returns the application instance for Gunicorn to use.

Now we should test if Gunicorn is able to serve the project. We do this by name of the entry point (module) i.e. `myapp`, and the name of the app or application factory, i.e. `factory`, along with other Gunicorn settings provided as command line flags or in your config file. We will also use a custom worker subclass that aiohttp provides. The end result should look like this:

    (env) [user@okcomputer]$ gunicorn myapp:factory --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker

Here we've also bound it to `0.0.0.0:8080`, so now you can visit your sever's IP address in the browser appended with 8080 and you should see I work!.

When you have confirmed that it works, you can close Gunicorn and deactivate the virtual environment.

### 0x300: Systemd Unit

The next thing to do is create a Systemd unit file so that when our server starts it automatically runs Gunicorn and serves our app. Create a unit file in `/etc/systemd/service/myapp.service`, where you can replace myapp with whatever your project is called.

```
[Unit]
Description=Gunicorn instance to serve myapp
After=network.target

[Service]
User=www
Group=www-data
WorkingDirectory=/var/www/myappdirectory
Environment="PATH=/var/www/myappdirectory/env/bin"
ExecStart=/var/www/myappdirectory/env/bin/gunicorn myapp:factory --bind unix:myapp.sock --worker-class aiohttp.GunicornWebWorker

[Install]
WantedBy=multi-user.target
```

In the `[Service]` we map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment). We'll then specify the commanded to start the service. Systemd requires that we give the full path to the Gunicorn executable, which is installed within our virtual environment.

Now we can start and enable the service:

    [user@okcomputer]$ sudo systemctl start myapp.service
    [user@okcomputer]$ sudo systemctl enable myapp.service

### 0x400: Nginx Conf

If you've noticed, in the Systemd unit, we've bound Gunicorn to `unix:myapp.sock`. Now Gunicorn should be waiting for requests to the socket file `myapp.sock` in our project's directory. We need to configure Nginx to to pass requests into this socket. Here is an example of a server block you can use:

```
server {
    listen 80;
    server_name myappdomain;

    location / { # checks for static file, if not found proxy to app try_files
        $uri @proxy_to_app;
    }

    location @proxy_to_app {
        include proxy_params;
        proxy_set_header
        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;
        proxy_pass http://unix:/var/www/myappdirectory/myapp.sock;
    }
}
```
