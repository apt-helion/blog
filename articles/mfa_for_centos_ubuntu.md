---
title: Adding 2FA For CentOS/Ubuntu Servers
category: development
date: 2019-01-22
thumbnail: 2fa-thumb.webp
tags: 2fa,centos,ubuntu
description:
---

This is a quick guide to set up two-factor authentication on CentOS/Ubuntu servers. By quick, I mean that I'm not going to explain much. I'm only writing this because I feel bad that I haven't made a post in over a month.

For this guide, we will be using the Google Authenticator app which you can download on your phone, although I think the PAM (Pluggable Authentication Module) also generates TOTPs compatible with Authy. So make sure you have one of those installed first.

Okay let's get started.

### Install Google's PAM

On CentOS:

    # Add the EPEL repo (if you haven't already)
    $ sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    # Install PAM
    $ sudo yum install google-authenticator

On Ubuntu:

    $ sudo apt-get install libpam-google-authenticator

Now run the initialisation app:

    $ google-authenticator

You'll be asked a few questions. I forgot what they where, so you're on your own with this, just read them and you'll probably be fine. After the first question a lot of output will scroll past, including a large QR code. At this point, use your authenticator app on your phone to scan the QR code or manually type in the secret key. Make sure you also record the secret key, verification code, and the recovery codes in a safe place.

### Configuring SSH

Open `/etc/pam.d/sshd` in the only good editor:

    $ sudo vim /etc/pam.d/sshd

And add this line to the bottom:

    ...
    auth required pam_google_authenticator.so

Now we need to configure SSH t support the authentication, open `/etc/ssh/sshd_config`:

    $ sudo vim /etc/ssh/sshd_config

Look for the `ChallengeResponseAuthentication` line. Change it from no to yes:

    ...
    # Change to no to disable s/key passwords
    #ChallengeResponseAuthentication no
    ChallengeResponseAuthentication yes
    ...

Restart SSH:

    $ sudo systemctl restart sshd.service

Now we can test if it works, open a new terminal session and attempt to SSH into it. If you don't use SSH keys, you're an idiot, but it should prompt for a verification code after you enter the password. If you're smart and previously created an SSH key, you'll notice you didn't have to type a verification code. This is because an SSH key overrides all other authentication options by default.

**The Next Part** will go through changing that to set up an SSH key as one factor and the verification code as a second.

### The Next Part

Open the sshd config file again and add the following line to the bottom:

    ...
    AuthenticationMethods publickey,password publickey,keyboard-interactive

Next, open the PAM sshd configuration file again. On CentOS, comment out this line:

    ...
    #@include common-auth
    ...

On Ubuntu, comment out this line:

    ...
    #auth substack password-auth
    ...

Now, restart the SSH service and test it again. If it all works, you should now call me your saviour who prevented you from getting hacked and losing millions of dollars because your developers have no idea what they're doing and setup their enterprise systems by following guides from shitty blogs.

You're welcome.

**Update 22/01/19:** My TravisCI deployment script was messed up because of this. But it was an easy fix, just [disable PAM for the user group TravisCI used.](https://askubuntu.com/questions/864986/disable-pam-module-for-group)
