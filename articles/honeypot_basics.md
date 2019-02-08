---
title: An Introduction to Honeypots/Honeynets
category: infosec
date: 2018-07-09
thumbnail: honeypot-thumb.png
tags: honeypot,honeynet
description:
---

A honeypot or a collection of honeypots (honeynet) is a controlled vulnerable system created to lure attackers. A honeypot appears to be a legitimate part of the site, but is actually isolated and monitored, and that seems to contain information or a resource of value to attackers. This allows honeypots to act as an early warning system, deceiving attackers, perhaps delaying and identifying them, and then ultimately supporting efforts to shut down the attack.

In general, you would use a honeypot to understand what is happening in key systems. If a web server is receiving thousands or millions of hits per day, it can be hard to differentiate between legitimate connections and attackers. Honeypots allow you to have a way to analyse attack traffic as your honeypot should have no legitimate users, allowing you to quickly identify attack traffic and create counter-measures.

There are 3 types of honeypots; low, medium and high interaction. Each type provides varying levels of security/detection difficulty, intelligence, and setup complexity. High interaction honeypots imitate the activities of the production systems that host a variety of services and, therefore, an attacker may be allowed a lot of services to waste their time. However, they use a lot of resources and can be complicated to setup. On the other hand, low interactions honeypots are easy to setup but provide the least amount of intelligence, as they only simulate the services frequently visited by attackers.

As an example, we will be looking at [Modern Honey Network (MHN)](https://www.anomali.com/platform/modern-honey-net), a honeypot management service by Anomali, which allows you to quickly deploy and manage honeypots. It utilises the HPfeeds protocol to centralise the data into a MongoDB instance for analysis.

MHN consists of a management server and one or more honeypots. The management server is where the honeypots send their data to, and creates a Flask app to make the data easily viewable from a web interface. A big advantage of MHN is it's simplicity and variety of honeypot deployment options. Honeypot deploy scripts include several common honeypot technologies, including:

* **Snort:** An open source intrusion prevention system capable of real-time traffic analysis and packet logging. It is not a honeypot per se, but an IDS/IPS, and is very helpful to detect attacks on your network. Sourcefire (the creator of Snort) was a acquired by Cisco but the product Snort remains open source.
* **Suricata:** An IDS/IPS much like Snort.
* **Dionaea:** A low interaction honeypot which exposes services like SMB, MSSQL, SIP, HTTP, FTP, TFTP. It is mainly used to trap malware exploiting vulnerabilities exposed by services offered to a network, and attempts to get a copy of it.
* **Glastopf:** A very popular Python web application honeypot that has the ability to emulate thousands of web vulnerabilities. It is no longer actively developed but it is "maintained" according to the developers.
* **Cowrie:** A medium interaction SSH and Telnet honeypot designed to log brute force attacks and the shell interaction performed by the attacker. It has SFTP support, SCP support, direct-tcpip (proxying) support and many other features.
* **p0f:** A tool that that uses passive fingerprinting to identify the OS behind a TCP connection.
* **Conpot:** A low interaction Industrial Control Systems honeypot and basically emulates some protocols used in industrial environments.
* **Wordpot:** A WordPress emulator honeypot which detects probes for plugins, themes, timthumb and other common files used to fingerprint a Wordpress installation.
* **ShockPot:** A web app honeypot designed to find attackers attempting to exploit the Bash remote vulnerability CVE-2014-6271.

From these, it should be easy to see the application of honeypots and their usefulness. However, as with any technology, there is no perfect solution. If compromised, a honeypot or honeynet can act as a springboard to launch additional system attacks to the "real" servers. In some cases, honeypots can decrease and organization's security by being more attractive to attacks and that the establishment of a vulnerable system can constitute as "gross negligence". In order for your honeypot to be effective, it must be monitored continually.
