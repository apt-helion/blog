---
title: Retro Exploits: Cross Site Tracing (XST)
category: infosec
date: 2018-06-22
thumbnail: xst-thumb.png
tags: xst,retro-exploits,xss
description:
---

In 2003, Microsoft attempted to protect against one of the most common forms of Cross Site Scripting by introducing the `HttpOnly` flag in Internet Explorer 6, which prevented cookies from being accessed by JavaScript. A common attack was to access the document.cookie object and send it to a web server controlled by the attacker so that they can hijack the victim's session. Tagging a cookie as httpOnly forbids JavaScript to access it, protecting it from being sent to a third party. Cross Site Tracing (XST) was discovered by Jeremiah Grossman in 2003, and is a method used to bypass this protection by using the TRACE HTTP method.

While this method is mostly deprecated now as modern browsers prevent TRACE methods from being made, I still think it's interesting to read about, and is simple enough to explain and allow me to practice blog writing. Now if you're thinking right now *'But this was only 15 years ago, why are you calling it retro'*? You are right, but you must consider that I was 3 years old when this was discovered, so it's pretty damn old for me.

The TRACE method, according to [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html), "allows the client to see what is being received at the other end of the request chain and use that data for testing or diagnostic information." Basically, it echos what is being sent to it for debugging purposes, allowing to see if the web server is malforming the request. The following is an example using cURL to form the header:

```bash
$ curl -X TRACE -H "X-Header: test" foo.com
TRACE / HTTP/1.1
User-Agent: curl/7.24.0
Host: foo.com Accept: */*
X-Header: test
```

As you can see it just sends the header back. Pretty harmless right? Well obviously not, because otherwise I wouldn't be writing about it. The problem is that TRACE will echo all the information you send to the server, this even includes cookies and Web Authentication strings as they are just headers as well.

```html
<script>
    var xmlhttp = new XMLHttpRequest();
    var url = 'http://foo.com/';

    xmlhttp.withCredentials = true; // send cookie header
    xmlhttp.open('TRACE', url, false);
    xmlhttp.send();

    xmlDoc=xmlHttp.responseText;
    alert(xmlDoc);
</script>
```

The above JavaScript code will send a TRACE request to the target web server. If the browser has a cookie from the target domain, the cookies will be shown on the alert. Of course this can be easily changed to do something more malicious such as sending the cookie to another server. XST successfully grants the code ability bypass `httpOnly` while accessing cookie data without the use of `document.cookie`.

Although this would no longer work on modern browsers, I still think it is important to know that even something seemingly harmless such as the TRACE method can be used as an exploit. If you want to read more about it, you can go through the [white paper](http://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf) for XST written by Jeremiah Grossman.

