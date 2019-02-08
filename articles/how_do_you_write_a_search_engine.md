---
title: How The Fuck Do You Write A Search Engine?
category: development
date: 2018-07-30
thumbnail: viperidae-thumb.png
tags: viperidae,python
description:
---

**Update 2019-01-25:** Much like [SPDS](/article/spds_release) I'm too lazy to maintain this, so it's now offline forever.

Following on with my previous article where we look at [old, shitty code and rebuild it](/article/how_do_you_write_a_blog), today we are looking at code I made for a school assignment. It was a search engine called 'viperidae' (I don't know how you are supposed to pronounce it) and was the first big software project I've ever done. You could even say that it was a MAJOR project... because it was. It was for my SDD Year 12 major project. But before we begin, I'll just get the question that everyone has right now out of the way.

**What mark did you get?**

95/100. I lost some marks because the parts of the documentation were lacking and because it only had 2 screens (there was a requirement for 3 screens, which is a STUPID requirement).

With that, we can now take a dive into the distant past of 2017.

This was my first repository on GitHub so you can go and look at it [here](https://github.com/beanpuppy/viperidae-old). Fun fact: if you look at the commit history (and ignore the terrible commit messages), you'll see that I actually started writing it a month (Dec 2016) before I was given the assignment (Jan 2017). I'm pretty sure that this is not allowed as you can't hand in anything you've created before the assignment is given, but as we all know: '*it's only cheating if you're caught*'.

Setting it up is pretty straightforward. Create a virtual environment, pip install requirements.txt, and then run run.py. If you did that then type 127.0.0.1:5000 in your browser's url bar which should show you this:

![image-alternative](/website/article/static/img/viperidae-old-start.png)

There are four fields to fill out here: search, depth, include external links, and seed. Unfortunately I don't have my original documentation which explained all of this and more, so I'll quickly explain why there are so many fields and what they do.

In case you don't know, writing a search engine is hard. Way too hard for any normal 17 year old, which caused me to cut a lot of corners. One of the biggest corners to cut was the entire 'index the entire web' part of a search engine. Because I was too dumb to understand any forms of concurrency or parallelism, I decided that I would not index any parts of the web because my web crawler was **WAYYYY** to slow. So it was decided that the web crawler would be a more integral part of the engine where the site was crawled during the search, instead of a precursor to it. This meant that in order to conduct a search, you also had to type in the website. This is the seed field. In the documentation I managed to frame this as '*creating more accurate searches by focusing on individual sites*'. Not the best excuse, but hey, anything for marks.

Now obviously I could have used something like Scrapy as a web crawler, which would have worked fifty billion times better than whatever I made. But I felt as though I was already using too many libraries and that I should write my own code. After all you wouldn't just import Essay would you?

However, that corner apparently wasn't cut enough. My crawler was still much too slow to crawl even a small website in a reasonable time. This is band-aided by the depth field which basically just limits how many pages are searched, which means I just let the user decide how long they want to wait.

The rest of the fields are just options for these round edges. search is obviously the item you want to search for and include external links determines if the crawler will crawl through links that aren't part of the seed website.

To be honest, that explanation covers pretty much everything I dislike about it. I've not really talked about the actual searching, but I don't expect myself to be able to create a super advanced algorithm to find exactly what you want. I just created something that worked well enough, as in it pointed you to a small house and said "ehhh it's somewhere in 'ere mate", ignoring the fact that you just asked for where it was in the small house.

Now is finally the time to look at the new search engine!

One of the big reasons I didn't like old viperidae was because it had no reason to exist as I had to hand wave a reason in the documentation. So now I've given the new on a real reason. It's a developer focused API for searching individual websites. It's a way for users to quickly create searching for their website with loads of special features. Although right now I haven't built any of the developer focused parts, I've built a redesign of the original engine. You can see a restricted, public demo [here](https://viperidae.app). If it were using the developer API, the website would already be indexed so the engine wouldn't have to crawl it. The API source is [here](https://github.com/beanpuppy/viperidae) and the source for the public website is [here](https://github.com/beanpuppy/viperidae-site).

This is all pretty bare bones right now because I've spent most of my time learning some new stuff while redesigning the engine. Namely the fact that the crawler is now asynchronous and is much faster than the original. Although it's still not Scrapy fast, it shouldn't really matter because the websites should be indexed anyway.

There is still a lot to do (pretty much all of it). But I'm sure in another year's time, I'll look back at it and decide that it's garbage and remake it all again.

**Update 2019-01-25:** Hey it's me from the top of the page, remember me? Anyway, ignore those last two paragraphs. Thank you.
