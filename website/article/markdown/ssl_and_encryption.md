---
title: SSL And Encryption
category: development
date: 2018-04-02
thumbnail: ssl-enc-thumb.png
tags: ssl,tls,encryption,centos,apache
description:
---

TLS (Transfer Layer Security) / SSL (Secure Socket Layer) are standard, cryptographic protocols that establish security over computer networks, between a web server and a browser. SSL provides a trusted environment where all data being transmitted is encrypted.

This article is technically a continuation of my [last article](/article/lamp_stack_on_centos) where we set up a CentOs7 server with Apache, and will go through explaining SSL aswell as setting it up our sever.

#### table of contents

* [TLS/SSL?](#0x100-tlsssl)
* [A Primer on Encryption and SSL](#0x200-a-primer-on-encryption-and-ssl)
* [The SSL Certificate](#0x300-the-ssl-certificate)
* [Let's Encrypt](#0x400-lets-encrypt)

### 0x100: TLS/SSL?

The terms SSL and TLS are often used interchangeably or in conjunction with each other (TLS/SSL), but one is in fact the predecessor of the other — SSL 3.0 served as the basis for TLS 1.0 which, as a result, is sometimes referred to as SSL 3.1.

As SSL was named by Netscape, the creators of the protocol, it was changed to TLS to avoid any legal issues with them so that the protocol could be "open and free". It also hints at the idea that the protocol works over any bidirectional stream of bytes, not just Internet-based sockets.

In order to prevent any confusion we will refer to TLS/SSL as just SSL from now on.

### 0x200: a primer on encryption and SSL

#### 0x201: asymertric and symmetric encryption

Asymmetric encryption (or public-key cryptography) uses a separate key for encryption and decryption. Anyone can use the encryption key (public key) to encrypt a message. However, decryption keys (private keys) are secret. This way only the intended receiver can decrypt the message.

Asymmetric keys are typically 1024 or 2048 bits. However, keys smaller than 2048 bits are no longer considered safe to use. Though larger keys can be created, the increased computational burden is so significant that keys larger than 2048 bits are rarely used. To put it into perspective, it would take an average computer more than 14 billion years to crack a 2048-bit certificate.

Symmetric encryption (or pre-shared key encryption) uses a single key to both encrypt and decrypt data. Both the sender and the receiver need the same key to communicate.

Symmetric key sizes are typically 128 or 256 bits, where a larger key is harder to crack. For example, a 128-bit key has `340,282,366,920,938,463,463,374,607,431,768,211,456` encryption code possibilities.

Whether a 128-bit or 256-bit key is used depends on the encryption capabilities of both the server and the client software. SSL Certificates do not dictate what key size is used.

#### 0x202: SSL

An SSL encrypted connection is generated through both asymmetric and symmetric cryptography through an SSL handshake. In SSL communications, the server’s SSL Certificate contains an asymmetric public and private key pair. The session key that the server and the browser create during the SSL Handshake is symmetric. In essence:

* The handshake begins when a client connects to an SSL-enabled server requesting a secure connection.
* The server then provides identification in the form of a digital certificate. The certificate contains the server name, the trusted certificate authority (CA) that vouches for the authenticity of the certificate, and the server's public encryption key.
* The client confirms the validity of the certificate before proceeding and then creates a symmetric session key and encrypts it with the server's asymmetric public key. Then sends it to the server.

This concludes the handshake and begins the secured connection, which is encrypted and decrypted with the session key until the connection closes. If any one of the above steps fails, then the SSL handshake fails and the connection is not created.

### 0x300: the SSL certificate

The SSL certificate is the most important component when generating an SSL connection between the client and server. Anyone can create a certificate, but browsers only trust certificates that come from an organization on their list of trusted CAs. Browsers come with a pre-installed list of trusted CAs, known as the Trusted Root CA store. In order to be added to the Trusted Root CA store and thus become a Certificate Authority, a company must comply with and be audited against security and authentication standards established by the browsers.

SSL Certificates will contain details of whom the certificate has been issued to. This includes the domain name or common name, serial number; the details of the issuer; the period of validity - issue date and expiry date; SHA Fingerprints; subject public key algorithm, subject's public key; certificate signature algorithm, certificate signature value. Other important details such as the type of certificate, SSL/TLS version, Perfect Forward Secrecy status, and cipher suite details are included. Organization validated and extended validation certificates also contain verified identity information about the owner of the website, including organization name, address, city, state and country.

For our server we will get an SSL certificate from Let's Encrypt, a free, automated, and open CA, run for the public’s benefit.

### 0x400: let's encrypt

The first step to using Let's Encrypt to obtain an SSL certificate is to install `certbot` on our server. But before we begin, we must will need to enable the `EPEL` repository, which provides additional packages for CentOS, including the `certbot` package we need. We will also need to install the `mod_ssl` module to correctly serve encrypted traffic.

    [user@okserver]$ sudo yum install epel-release
    [user@okserver]$ sudo yum install mod_ssl python-certbot-apache

#### 0x401: requesting a certificate

Using certbot to generate a certificate is quite easy. The client will automatically obtain and install a new SSL certificate that is valid for the domains provided as parameters. To execute the interactive installation and obtain the certificates, run the certbot command with:

    [user@okserver]$ sudo certbot --apache -d YOUR_DOMAIN -d OPTIONAL_DOMAIN

We will be presented with a step-by-step guide to customize our certificate options. We will be asked to provide an email address for lost key recovery and notices. If our Virtual Host files do not specify the domain they serve explicitly using the ServerName directive, we will be asked to choose the Virtual Host file (the default ssl.conf file should work).

That's pretty much it. The generated certificate files should be available within a subdirectory named after your base domain in the /etc/letsencrypt/live directory. However, as the default SSL configuration shipped with CentOS's version of Apache is a bit dated and as such, it is vulnerable to some more recent security issues and is recommended that we select more secure SSL options. I suggest going through Remy van Elst's [tutorial](https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html) on strong SSL security on the Apache2 webserver, as it does a better job of explaining it's solutions than I would.
