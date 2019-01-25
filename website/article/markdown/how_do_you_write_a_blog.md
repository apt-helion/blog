---
title: How the Fuck Do You Write a Blog?
category: development
date: 2018-05-30
thumbnail: blog1.0-404-thumb.png
tags: blogpost
description:
---

So far this blog has averaged 0.6 articles per month (including this one) since it was launched in Feburary. Normally you would assume this is just because I'm lazy or that my social anxiety prevents me from writing anything on the internet because of a constant fear of judgement. And normally you'd be right, and you are. But it's also because of something else.

When I was first creating this blog, I wanted to make everything from scratch (the idiom, not the language) and I really do mean EVERYTHING. Flask? Literally any web framework? Why would I need that when I have Jinja and CGI? URL endpoints? HAH! I could just use the Apache config to map everything! Bootstrap?? WHAT A JOKE! I DON'T NEED THAT! I'M A CSS MASTER!

Obviously this was a terrible idea that came from my original plans to have the entire website emulate the command line (which is also a terrible idea that I also have no idea how to do). So now four months later, we will look at the old site and laugh at how stupid I was.

Right before I wrote this article, I mapped the old site on the Wayback Machine so you could go and [look at all 8 pages here.](https://web.archive.org/web/20180529040508/https://blog.justinduch.com) You can also see the source code up to the final commit before this redesign [here.](https://github.com/apt-helion/blog/tree/484e9c3d808e08ab41605a3c8a36c4793ba49274) I've also included some pictures in case you were to lazy to click on those.

#### table of contents

* [The Looks](#0x100-the-looks)
* [The Logic](#0x200-the-logic)
* [The Redesign](#0x300-the-redesign)
* [What's Next](#0x400-whats-next)

### 0x100: The Looks

There isn't too much to say here apart from: 'it isn't very nice'. It was my first time using CSS grid in any real capacity, and while I do like it - probably more than Bootstrap, I wasn't able to do very much with my more limited CSS knowledge. You can see I had my original plans in mind while desiging it, with all it's plain-ness, but not a good minimalist plain, the bad, uninteresting plain.

![image-alternative](/article/static/img/blog1.0-root.png)

Figure 0: The homescreen with the tree style web page directory.

Let's just start with the homepage `/`. It's actually okay in my opinion, probably the best page in the site. The tree style directory map looks decent in the center, making the command line design inspiration very clear. Overall I don't hate it, although it is useless because no one would need to go to it.

![image-alternative](/article/static/img/blog1.0-articles.png)

Figure 1: The `/articles` page

Clicking on articles takes us to `/articles` and now we face the horror. This is pretty much what the entire site looks like. A harsh contrast of black and white making it very tough on the eyes. The command line design continues with the header showing a nice 'pwd' which displays your current directory. The tree style pages do not suit the format of a sidebar, and makes it look out of place. If you click on an article, you can see that the sidebar will grow along with the length of the article, but the tree will stay at the top, making the left side wasted space. The design is pretty utilitarian (in the bad way) and makes no attempt to please the reader.

That's all I have to say about the asthetics, I don't know how to properly critque this. I'm not a designer by any means and this should have shown you why.

### 0x200: The Logic

Here is the real monster, the reason I haven't bothered to write any posts, and maybe even my worst attempt at designing a piece of software I've ever written. I'm not sure on where to even start, so many things are just wrong and inefficent.

How about the things I didn't do? Continuing on from the intro, I didn't use any web frameworks with only Jinja as a templating engine and pure CGI magic with Apache rewrite rules to change the URL.

What does this mean? It means that in order to get the blog's content to do what I wanted (which was to have each article be accessible from it's own URL instead of using a GET request with an ID for the database) the articles had to be in the html folder for Apache to serve them to the user. And since these articles were in the html folder and not cgi-bin, Jinja could not render them, which meant I had no templating for my articles. Of course this then meant that everytime I would have to make a change to the general layout of the blog, I would have do it to the layout for Jinja templating as well as every article in the html folder. Oh no.

My cgi-bin scripts also suffered from this as I had to rewrite the URL for each page. Here's a small peak of my Apache config (since it isn't on GitHub).

    RewriteEngine On
    RewriteRule ^/$ /index.html [PT] # Fix later
    RewriteRule ^/articles/$ /app/articles [PT]
    RewriteRule ^/articles/security$ /app/security [PT]
    RewriteRule ^/articles/misc$ /app/misc [PT]
    RewriteRule ^/info$ /app/info [PT]
    RewriteRule ^/contact-me$ /app/contact [PT]

Yeah, it isn't pretty. Note the fix later comment.

This caused me a lot of work to be done on even the tinyest change, and really put me off on working on it. That is until I decided to burn it and start again.

### 0x300: The Redesign

What you are reading now is blog 2.0, the redesign. I've made many improvements to make the website better to view and develop. The biggest change as you can imagine is the use of an actual web framework. The blog uses [simplerr](https://github.com/yevrah/simplerr), a framework one of my co-workers made, and one that I find easier to use than Flask (although that may be because I've used it more). It's also using a Bootstrap template, so no more plain ugly.

All of this and more such as the tagging system have been made 1 day faster (2 days) than what blog 1.0 took (3 days), which really shows how much easier using other people's stuff is. Obviously, there's much more to improve, but that is mainly on my side to make it easier to manage/write articles.

### 0x400: What's Next

A big feature that's standard of every blogging site is the ability to write articles on the site and then uploading it to the database. Right now I write it in HTML using Vim and then manually edit the database. This is pretty inefficent and it wouldn't be too hard to add a text editor to the site, but right now I do not want to deal with authentication (so that only I can see and upload in progess articles), so this feature is on hold. I simply do not post enough for this to be a major problem right now ;)

**Update 2018-05-31:** jks nvm that was easy. I didn't need auth, just set an environment variable for the production server, so you can only edit articles on dev machines.
