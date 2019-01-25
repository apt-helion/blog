---
title: HackTheBox - Dev0ops
category: infosec
date: 2018-10-15
thumbnail: dev0ops-thumb.png
tags: htb
description:
---

The first box I've ever done (Jerry doesn't count because it was piss easy) has been retired a few days ago, so now let's go through how I solved it.

![image-alternative](/common/static/img/dev0ops-nmap.png)

The nmap scan shows it's running Gunicorn on port 5000. Web apps are always fun, and it's even using tech I've dabbled in before. Anyway we should open it in a browser.

![image-alternative](/common/static/img/dev0ops-website.png)

Not much to go on here apart from the fact that it's supposed to be a blog. Let's run gobuster on it to see if there is anything else.

![image-alternative](/common/static/img/dev0ops-gobuster.png)

The scan hasn't completed yet but we've already found some interesting urls so we can forget about it and leave gobuster in the background for now. `/feed` is just the image at the bottom of the main page you see up top, the important one is `upload`.

![image-alternative](/common/static/img/dev0ops-upload.png)

As you can see it's just a way to upload new posts as XML. Let's try and upload something. The format of the XML file is given to us as Author, Subject, and Content. Also note the capitalisation, which is actually important because it won't accept it with lowercase (I wasted over 30 mins trying to figure out why it wouldn't accept it). Here is our test XML (the name of the parent tag also doesn't matter):

```xml
<file>
    <Author>test</Author>
    <Subject>test</Subject>
    <Content>test</Content>
</file>
```

![image-alternative](/common/static/img/dev0ops-upload-test.png)

So it just processes it and displays it back. It should be pretty obvious now that all we need to do is an XML injection to read the filesystem. We can get `user.txt` like this without ever having to actually access the server. This is the payload to use:

```xml
<!DOCTYPE foo [ <!ENTITY Subject ANY >
    <!ENTITY xxe SYSTEM "file:///home/roosa/user.txt" >
]>

<file>
    <Author>test</Author>
    <Subject>&xxe;</Subject>
    <Content>test</Content>
</file>
```

Basically, we are creating an external entity named `xxe` which forces the XML parser to access the resource specified by the URI **"file:///home/roosa/user.txt"** which I got from the **"File path:"** field which is displayed when we uploaded our test XML.

![image-alternative](/common/static/img/dev0ops-user.png)

Uploading it gives us user in the subject field.

Now looking at files from the filesystem is neat and all, but it isn't going to give us root. We're definitely going to need to find a way to get a shell. The first thing I did was get `/etc/passwd` which was fine, but I was unable to get `/etc/shadow` presumably because the Gunicorn instance doesn't run as root, so my plan of cracking root's password was foiled.

After a bit of thinking and looking at random files, I went back to the nmap scan saw ***THE ANSWER***. Here is the new payload:

```xml
<!DOCTYPE foo [ <!ENTITY Subject ANY >
    <!ENTITY xxe SYSTEM "file:///home/roosa/.ssh/id\_rsa" >
]>

<file>
    <Author>test</Author>
    <Subject>&xxe;</Subject>
    <Content>test</Content>
</file>
```

Here we are just taking the user's SSH private key, so we should hopefully be able to sort of impersonate them and SSH into the box without a password.

![image-alternative](/common/static/img/dev0ops-sshkey.png)

Nice! Now we can save it into a file and SSH into the box. But first we need to format it and then give the the correct permissions. I used [this tool](https://www.samltool.com/format_privatekey.php) to format the key and edited the permissions with (where ssh_rsa is our private key file):

    chmod 400 ssh_rsa

This only gives root access to the file (which is us) because SSH requires that is is not editable by other users. Now we force SSH to use our private key file.

![image-alternative](/common/static/img/dev0ops-sshin.png)

And we're in! Now for privesc.

Normally the first thing I do when given shell is look at their bash history.

![image-alternative](/common/static/img/dev0ops-bash-history.png)

Apart from using an inferior text editor (emacs was also being used further down), the thing that stands out the most is Git, which is also very familiar to me. The Git repository is in `~/work/blogfeed`, so let's go there and look at the Git logs with git log.

![image-alternative](/common/static/img/dev0ops-git-log.png)

There's a very interesting commit there with the message "reverted accidental commit with the proper key". Could they be talking about the private key for root? Let's look at the commit before it (which should be the commit where the not 'proper key' is added instead of deleted) with git show <commit\_hash> where **commit\_hash** is the commit's hash: `d387abf63e05c9628a59195cec9311751bdb283f`.

![image-alternative](/common/static/img/dev0ops-git-mistake.png)

Look at that! It's a private key. Now to be completely clear, I have no idea if this is actually root - this is all total guess work, but let's try it anyway. Save it to a file, change the permissions, you know the rest.

![image-alternative](/common/static/img/dev0ops-root.png)

It worked! You can find root.txt in /root.

