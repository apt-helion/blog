---
title: Goodbye Google
category: development
date: 2019-06-20
thumbnail: gg-thumb.png
tags: google,blogpost
description:
---

Today I've removed every single trace (I think) of Google from this website
because... I shouldn't need to explain this right? I'm sure you know the
reason.


It wasn't that hard, there were only four things I was using, and in
some cases there was an improvement in functionality when switching to a
different provider. Lets go through all four of them now:

### Google Analytics

This one is simple, I removed this script tag from the page layout.

```
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-114590042-1"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-114590042-1');
</script><Paste>
```

This hasn't been replaced though because I don't really care about how many
people visit this site anymore.

### Google Fonts

Previously I was serving fonts from `fonts.googleapis.com` because I wasn't
bothered to download them and serve them myself.

```
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Herr+Von+Muellerhoff">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato:300i,300,400i,700,700i">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Libre+Baskerville:400i,700">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lora">
```

I've also taken this time to remove `Lora` from my fonts (because you
shouldn't use more than 3 fonts styling wise) and clean up some css, so the
site should be **slighlty** faster now.

### GSuite

I don't even know why I chose to use Google for delivering emails but it
doesn't matter now anyway. I've switched to Sendmail, and while I don't really
like Twilo (Sendmail's parent company) either, there's a few advantages to
this:

* I can use my propery domain; Where previously I would send emails from
`noreply@noreply.justinduch.com` because Google requires domain verification
and my MX records for `justinduch.com` point to Protonmail, meaning I needed
to use a different subdomain. Now I can use `noreply@justinduch.com` because
Sendmail doesn't required domain verification.

* It's free for the first 100 emails a day, so as long as I don't get over 100
subscribers, I won't need to pay.

* Not Google.

Also GSuite seems to have a few [issues][].

The only other option I could see was managing a SMTP server myself and that
seems like a pain in the ass.

[issues]: https://reddit.com/r/sysadmin/comments/c2lane/g_suite_repeated_outages/

### WebP Images

This one probably doesn't matter as much, but for the past week I've been
tampering with different image types to see if it would speed up the load
times. Moving to WebP didn't actually do all that much and it cost me Safari
support, so I've just moved back to pngs.
