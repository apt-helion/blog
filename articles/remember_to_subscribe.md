---
title: And Remember To SMASH That Subscribe Button
category: development
date: 2018-09-15
thumbnail: subscribe-thumb.png
tags: blogpost,python
description:
---

A few days ago someone asked if I had a subscribe feature for this blog where I would email people every time I posted something, so I told them:

*'No, that's a shit idea, why would I want to make it easier for people to read my poorly written rants?'*

However, it's currently 01:00 in the morning and I've been attempting privilege escalation on the HTB box SecNotes for over 7 hours now trying to get this STUPID FUCKING **<redacted for spoilers>** TO WORK AND I DON'T EVEN KNOW IF IT'S WHAT I'M SUPPOSED TO DO. I MEAN I MANAGED TO GET A **<redacted for spoilers>** WORKING EXCEPT IT DOESN'T ACTUALLY WORK FOR SOME REASON I DON'T KNOW WHAT THE FUCK EVEN IS THIS.

So I think it's time to do something different.

If you go to the [home page](/) now and scroll to the bottom, you will see a field where you can enter your email to subscribe and be notified every time I post and article! Just make sure to verify your email after you enter it.

Ok that's all. Thanks everyone, goodbye.

...

Oh of course that's not actually the end silly! This is a tech blog after all, and I am legally required to explain how it works even though it's incredibly simple and no one cares. So let's get right into it.

In order to actually send the emails I'm using an edited version of [this script](https://github.com/ludmal/pylib/blob/master/mail.py) which made the process pretty simple, making the majority of my work focused on the verification and unsubscribing portions. Both of these as you would imagine are just uuids I assign to each email and send through with each link.

Now with the emails themselves, you may have noticed that they are being sent from 'noreply@noreply.justinduch.com' instead of my actual *business* email which is 'justin@justinduch.com'. This is because Protonmail, the email server I am using, does not support IMAP/SMTP currently. I've had to create new domain records for 'noreply.justinduch.com' in order to point MX records to the Google SMTP servers, which is obviously not ideal but there's not much I can do.

The actual email content is in HTML, although I was too lazy to actually write it myself I just used [BEE Free](https://beefree.io/) to make them for me (not advertising or anything, they were literally the first search result for 'html email editor'). I think the email itself looks fine, but if you look at the source code for these emails, the combination of not having the ability to put CSS in separate files and generated code from some website makes it's a pretty ugly site to see.

I think that just about wraps it up. Like I said, pretty simple and uninteresting. So that's it for real now. Goodbye.

...

SIKE! Did you forget that this actually a security-focused tech blog? The one thing that was constantly going through my mind as I wrote this service up (for reasons completely unrelated to previous events) was: *'can this be hacked?'*

The answer to that, as always is:

*'Uh, yeah... pr-probably.'*

While writing it I attempted to identify the most likely things that could be vulnerable. Which were obviously SQLi and XSS, but because I'm kinda tired right now, I'm just gonna get SQLi out of the way: No, you can't, peewee santises everything.

So let's try to XSS the initial subscription page, which shows you your email after you enter it on the next page. We will just put in a basic `<plaintext>` tag.

![image-alternative](/website/article/static/img/subscribe-plaintext.png)

Oh no! It only accepts correct email addresses and stops us from submitting our code! Looks like this is unhackable...

Is what an idiot would say. This shitty client side validation is no match against my best friend Burp Suite. We'll just give the input a correct value and my buddy will intercept the request and change it to the value we actual want.

![image-alternative](/website/article/static/img/subscribe-burb.png)

Wow. I wish I could intercept like Burp.

![image-alternative](/website/article/static/img/subscribe-fail.png) Oh. It didn't work and looking at the logs, it looks like it failed correctly.

![image-alternative](/website/article/static/img/subscribe-error.png) Looks like this is it then. The real end. It's been a good ride, have a great night everyone.

...

But I hear you ask: *'Isn't this also a fashion blog?'*

No. That was a one time thing. I'm serious now this is the end.

