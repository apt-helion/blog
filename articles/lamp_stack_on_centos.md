---
title: Setting up a LAMP Stack on CentOS 7
category: development
date: 2018-01-22
thumbnail: lamp-stack-thumb.png
tags: linux,centos,apache,mysql,python
description:
---

Welcome to the first post of my blog! This article will teach you how to set up a LAMP Linux(CentOS), Apache, MySQL, Python web server from scratch, just like how I did to get this blog running. This guide will go through everything and not all of it may apply to your circumstance, so feel free to skip ahead using the table of contents.

#### Table of Contents

 * [The DNS and Web Server](#0x100-the-dns-and-web-server)
 * [Initial Server Setup](#0x200-initial-server-setup)
 * [AMP'ed up](#0x300-amped-up)
 * [The Apache Config](#0x400-the-apache-config)

### 0x100: the DNS and web server

The DNS (Domain Name System) is a system that resolves a server's domain name eg. blog.justinduch.com into an IP address. In order for your pngage to be viewable, you must point your domain name to the webserver.

As this process is different for every domain name registrar and server provider it is up to you to find the documentation to do this for your specific setup. Once you have a sever and domain name aswell as pointed them, we can continue with the guide.

### 0x200: initial server setup

Once you have your new server, you can log into it through SSH with it's public IP address. On Linux/Mac machines, use the command:

    [user@okcomputer]$ ssh root@SERVER_IP

or connect through PUTTY on a Windows machine.

#### 0x201: adding a new user

Now you are logged in as the root user, which is the administrative user in a Linux environment and is given heightend privilages. Because of this, we will create a new user that we will use to log in from now in order to help prevent making any destructive changes on accident.

    [root@okserver]# useradd USER_NAME

Now you can assign the user a password:

    [root@okserver]# passwd USER_NAME

Our new user has been set up, but it only has regular user privilages. If we ever want to do administrative tasks on the server (like installing packages in the later sections), our regular user will be denied access. To avoid having to go back to root, we can set up our user as a 'super user'. This allows the user to run commands with root privilages by adding sudo before each command.

To do this we will add our user to the wheel group. By default, on CentOS, members of the wheel group have sudo privileges.

    [root@okserver]# usermod -aG wheel USER_NAME #### 0x202: configuring ssh

To make our server more secure we will configure the SSH daemon to disallow remote SSH access from root and change the deafult SSH port. Changing the default port from 22 to someting more unique will help to stop many automated attacks, and make it harder to guess which port SSH is accessible from. You can enter any port number from 1024 to 32,767.

Open the configuration file on your text editor eg. vi or nano:

    [root@okserver]# vi /etc/ssh/sshd_config

Look for the lines:

    ...
    Port 22
    ...
    #PermitRootLogin yes

and change them to:

    ...
    Port YOUR_PORT_NUMBER
    ...
    PermitRootLogin no

Now that we have made our changes, we will restart SSH and test our configuration:

    [root@okserver]# systemctl restart sshd.service

Open a **new** terminal window (do not disconnect from the old session until we can verify that the config works) and connect with the command:

    [user@okcomputer]$ ssh -p PORT user@SERVER_IP

You should now be logged in as your new user through the new SSH port. If your server has a firewall you may also want to allow TCP connections through the new port and block the old port.

### 0x300: AMP'ed up

With our server configured we can now go through the the final 3 letters of the LAMP stack.

Before we install anything we should update the system:

    [user@okserver]$ sudo yum -y update

Remember that we need to use `sudo` from now on to gain root privilages!

From now on this guide will use vim instead of vi as it's text editor, to install vim enter:

    [user@okserver]$ sudo yum install vim

#### 0x301: a for apache

Install Apache with:

    [user@okserver]$ sudo yum install httpd

Now you can start and enable the service:

    [user@okserver]$ sudo systemctl start httpd.service
    [user@okserver]$ sudo systemctl enable httpd.service

#### 0x302: m for mysql

We are actually installing `MariaDB` for our database, but it still starts with a 'm' so it counts.

    [user@okserver]$ sudo yum install mariadb mariadb-server

Start and enable it:

    [user@okserver]$ sudo systemctl start mariadb
    [user@okserver]$ sudo systemctl enable mariadb

Now you will want to set up the database. Add a root user with:

    [user@okserver]$ mysqladmin -u root password PASSWORD

You can test it by connecting to the database with:

    [user@okserver]$ mysql -u root -p

#### 0x303: p for python

CentOS actually comes with Python2.7 by deafult, so if you are one of those neanderthals who still use 2.7 you can skip this step. For the rest of us intellectuals, you will need to install install IUS, which stands for Inline with Upstream Stable. IUS provides the Red Hat Package Manager (RPM) packages for some newer versions of select software.

    [user@okserver]$ sudo yum install https://centos7.iuscommunity.org/ius-release.rpm

Now you can install Python3:

    [user@okserver]$ sudo yum install python36u

You may also want to install pip and the development package needed for the mysqldb module:

    [user@okserver]$ sudo yum install python36u-pip python36u-devel

Now your LAMP stack is installed! The next section goes through the Apache config to get you to the testing page.

### 0x400: the apache config

This section will go through how to get a set up a virtual host in Apache. You can choose many different ways to set up a virtual host, this guide will show the way I did it.

Create the required directories for the website:

    [user@okserver]$ sudo mkdir /var/www/YOUR_DOMAIN
    [user@okserver]$ sudo mkdir /var/www/YOUR_DOMAIN/cgi-bin
    [user@okserver]$ sudo mkdir /var/www/YOUR_DOMAIN/html
    [user@okserver]$ sudo mkdir /var/www/YOUR_DOMAIN/conf

`cgi-bin` is the directory where you will keep your scripts.

`html` is the document root for Apache.

`conf` is the directory where your virtual host config is placed.

Now create `vhost.conf` in the `conf` directory:

    [user@okserver]$ sudo touch /var/www/YOUR_DOMAIN/conf/vhost.conf

and edit it:

    [user@okserver]$ sudo vim /var/www/example.com/conf/vhost.conf

Here is a very basic example where example.com is my domain name:

    <VirtualHost *:80>
        ServerAdmin admin@example.com
        ServerName example.com
        ServerAlias /app/ "/var/www/example.com/cgi-bin/"
        DocumentRoot /var/www/example.com/html
    </VirtualHost>

Now we can edit the Apache config to include this virtual host config:

    [user@okserver]$ sudo vim /etc/httpd/conf/httpd.conf

and this line to the end of the file:

    Include /var/www/example.com/conf/vhost.conf

Restart Apache with:

    [user@okserver]$ sudo apachectl graceful

That's it! You can test if your web server works by typing your domain into the browser, which should direct you to Apache's testing page. For more config options see the [official documentation.](https://httpd.apache.org/docs/2.4/vhosts/)
