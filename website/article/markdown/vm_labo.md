---
title: I Put A Bunch Of VMs Together And Call It A Lab
category: infosec
date: 2018-12-14
thumbnail: labo-thumb.png
tags: vm,lab
description:
---

During the past few days, I've been setting up virtual machines to use for demonstrations on this blog. It's very basic, two Windows boxes and a Linux server and although I originally wanted a Windows server as well, those plans where short lived after I saw the price for a license.

All of the VMs are stored on a 250GB external SSD (because my MacBook has zero space on it) and are accessed from VMware Fusion disconnected from the internet and in a virtual private network.

While the configuration and firewall/anti-virus stuff will constantly change, I'll probably mainly only use this for malware analysis so I've pre-installed some software to use. On the Windows boxes, there's Python and a debugger, and on the Linux box I've installed INetSim to simulate common internet services and Wireshark (you should know what this does). Just realising now that I should also give it a Samba share...

I've also created another box in the network to carry out any pen testing I may do. It runs Parrot OS as opposed to Kali (hence the thumbnail). I've never touched it before this, so I'm intrigued to see how it differs to Kali. If it's not much of a pain, I may also consider switching my main pen testing VM to Parrot.

Anyway here's the list of the boxes.

|| OS || IP || HOSTNAME ||
|| Windows 7 x86 || 192.168.1.70 || RIOTDIVISION ||
|| Windows 10 x64 || 192.168.1.50 || ROSEN ||
|| Lubuntu 10.14 x64 || 192.168.1.100 || ANDWANDER ||
|| Parrot 4.4 x64 || 192.168.1.20 || ACRONYM ||

And yes, I did name them after clothing companies. What did you expect? This is a fashion blog after all.

