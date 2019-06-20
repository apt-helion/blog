---
title: HackTheBox Notes - Curling (ft. Anger)
category: infosec
date: 2019-04-01
thumbnail: curling-thumb.png
tags: htb,htb-notes
description:
---

Continuing from [last time](/article/htb_hawk) where I just post my notes,
today is `Curling`. Also note that today is the first of April, and my April
fools joke is that this is not an April fools joke… or is it? I jest of
course, these notes are already enough of a joke.

- - - -

### Nmap Scan
```
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-05 09:58 AEDT
Nmap scan report for 10.10.10.150
Host is up (0.49s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 8a:d1:69:b4:90:20:3e:a7:b6:54:01:eb:68:30:3a:ca (RSA)
|   256 9f:0b:c2:b2:0b:ad:8f:a1:4e:0b:f6:33:79:ef:fb:43 (ECDSA)
|_  256 c1:2a:35:44:30:0c:5b:56:6a:3f:a5:cc:64:66:d9:a9 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: Joomla! - Open Source Content Management
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.14 seconds
```
### Joomla! Site
`http://10.10.10.150`

* Has upload button at bottom of all pages
* `http://10.10.10.150/administrator/manifests/files/joomla.xml` shows version is `3.8.8`. Released May 22 2018
* Page `/secret.txt` displays `Q3VybGluZzIwMTgh`. Tried this as password on `/administrator` with user `admin` but nope.
	* It’s actually base64. Decodes into `Curling2018!`. Still doesn’t work with `admin`
	* Found username `Floris` in one of the articles. Worked with `Curling2018!`
* Looked at
[this](http://www.thehackerstore.net/2015/01/how-to-upload-shell-in-joomla-via-admin.html)
to upload a PHP shell from [this](https://github.com/pentestmonkey/php-reverse-shell)
	* Created new file in templates `hello.php` and put shellcode there
	* Run `nc -lvpn <port_number>`
	* Go to `10.10.10.150/templates/beez3/hello.php`
	* Got shell as user `www-data`

### PHP Reverse Shell
* Can’t get `user.txt` because we don’t have permissions for `~/floris` but we
can view another file `password_backup`[^1]. It’s a hexdump for something…
* This [list of file
signatures](https://en.wikipedia.org/wiki/List_of_file_signatures) tells us the file is a `bz2` file because it has the signature `42 5A 68` at the start
* Went to `/var/www/html/bin` because the user has write permissions there
* Copied `/home/floris/password_backup`
* Reversed the hexdump back to a `bz2` file with `xxd -r password_backup password_backup.bz2`
* Decompressed the file `bzip2 -d password_backup.bz2`
* Contains the string
```
l[passwordrBZh91AY&SY6@@Pt t"dhhOPIS@68ET>P@#I |3x(*N&Hk1x"{]B@6m
```
What is this

* Did a `file` on it
`password_backup: gzip compressed data, was "password", last modified: Tue May 22 19:16:20 2018, from Unix`
Oh it’s zipped again

* Added `.gz` as a file extension and unzipped it
```bash
$ gunzip password_backup.gz
$ cat password_backup
BZh91AY&SY6@@Pt t"dhhOPIS@68ET>P@#I |3x(*N&Hk1x"{]B@6
```
WHAT THE FUCK IS THIS

* Checked `file` again
```bash
$ file password_backup
password_backup: bzip2 compressed data, block size = 900k
```
This is getting really annoying

* OK
```bash
$ mv password_backup password_backup.bz2
$ bzip2 -d password_backup.bz2
$ cat password_backup
password.txt0000644000000000000000000000002313301066143012147 0ustar  rootroot5d<wdCbdZu)|hChXll
```
Fucks sake
```bash
$ type password_backup
password_backup: POSIX tar archive (GNU)
```
Ugh

* Maybe this will be the last time…
```bash
$ mv password_backup password_backup.tar
$ tar -xvf password_backup.tar
password.txt
```
THIS IS IT!!!
```bash
$ cat password.txt
5d<wdCbdZu)|hChXll
```

### SSH Server
`ssh://10.10.10.150:22`

* Logged in `floris@10.10.10.150` with password `5d<wdCbdZu)|hChXll`
* Get user `cat user.txt`. What a fucking pain
- - - -
* Folder `~/admin-area` has files `input` and `report`
	* Whenever one is edited it is reverted back a while later by something
	* `ls -al` shows it’s being edited every minute. I’m, pretty sure we’re dealing with cron here
* Had a guess that a cron job was calling `curl` with a url from the file `input` and redirecting the result to `report`
	* Changed the url in input from `http://127.0.0.1` to `file:///home/floris/user.txt`
	* Wait for the start of the next minute and `report` now has the user hash. So yep, i’m right
* Changed url  to `file:///root/root.txt` (probably should have done this as
the first test)
* And now we wait…

```bash
floris@curling:~/admin-area$ date
Mon Nov  5 06:52:01 UTC 2018
floris@curling:~/admin-area$ ls -al
total 16
drwxr-x--- 2 root   floris 4096 May 22 19:04 .
drwxr-xr-x 7 floris floris 4096 Nov  5 06:51 ..
-rw-rw---- 1 root   floris   25 Nov  5 06:52 input
-rw-rw---- 1 root   floris   33 Nov  5 06:52 report
floris@curling:~/admin-area$ cat report
82c198ab6fc5365fdc6da2ee5c26064a
```

There must have been a way to find out that cron was using curl instead of pure guesswork, but oh well.

### Footnotes
[^1]:
```
00000000: 425a 6839 3141 5926 5359 819b bb48 0000  BZh91AY&SY...H..
00000010: 17ff fffc 41cf 05f9 5029 6176 61cc 3a34  ....A...P)ava.:4
00000020: 4edc cccc 6e11 5400 23ab 4025 f802 1960  N...n.T.#.@%...`
00000030: 2018 0ca0 0092 1c7a 8340 0000 0000 0000   ......z.@......
00000040: 0680 6988 3468 6469 89a6 d439 ea68 c800  ..i.4hdi...9.h..
00000050: 000f 51a0 0064 681a 069e a190 0000 0034  ..Q..dh........4
00000060: 6900 0781 3501 6e18 c2d7 8c98 874a 13a0  i...5.n......J..
00000070: 0868 ae19 c02a b0c1 7d79 2ec2 3c7e 9d78  .h...*..}y..<~.x
00000080: f53e 0809 f073 5654 c27a 4886 dfa2 e931  .>...sVT.zH....1
00000090: c856 921b 1221 3385 6046 a2dd c173 0d22  .V...!3.`F...s."
000000a0: b996 6ed4 0cdb 8737 6a3a 58ea 6411 5290  ..n....7j:X.d.R.
000000b0: ad6b b12f 0813 8120 8205 a5f5 2970 c503  .k./... ....)p..
000000c0: 37db ab3b e000 ef85 f439 a414 8850 1843  7..;.....9...P.C
000000d0: 8259 be50 0986 1e48 42d5 13ea 1c2a 098c  .Y.P...HB....*..
000000e0: 8a47 ab1d 20a7 5540 72ff 1772 4538 5090  .G.. .U@r..rE8P.
000000f0: 819b bb48                                ...H
```
