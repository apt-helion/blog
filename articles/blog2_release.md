---
title: I Finally Finish This Blog's First Production Release
category: development
date: 2019-01-24
thumbnail: blog2-thumb.webp
tags: blogpost
description:
---

I've been developing this website for just under a year now, with it having a [major revision](/article/how_do_you_write_a_blog) three months in. But now it's finally ready for it's production release, as in, I finished developing every feature a blog needs (or only the ones I wanted). So what was the last feature you ask?

It was that search bar on the top right.

That's right, the search bar hasn't worked for the past year even though it looks so inviting, and looking at my Google Analytics report, it has fooled a few of you. Anyway, even though [I've made a search engine](/article/how_do_you_write_a_search_engine) in the past, I thought it was too much of a bother to do, so the bar just turns it into a Google search. Literally five lines of HTML.

## the future

Now, to celebrate this ***momentous*** achievement, here's a look into notes I have of future blog developments.

![image-alternative](/website/article/static/img/blog2-future.webp)

Neat stuff. Let's go through them and I'll explain why I'll probably never get them done.

#### Get better web.dev score

[web.dev](https://web.dev) is an "automated tool for running diagnostics on any web page—will help you understand how and where to start improving the quality of your web page. It has audits for performance, accessibility, progressive web apps, and more."

I think my score is around 75/100, which is not very good.

#### Refactor peewee models

I am too lazy to do this, it works fine for now.

#### Find better way to send emails

Currently whenever a new article is posted, I manually log into my server and run a script to send emails to everyone. This is bad and I don't like it. I've tried thinking of ways to get it to work with it's auto-deployment to TravisCI, but because of how I've structured writing and publishing articles, it's too much effort. I may have to write a script that runs the script on the server...

#### Add liking function to articles

This would be easy (as for the note, I would just store what a reader has liked in localstorage), but I'm probably not going to do it for reasons explained below.

#### Add analytics page

I think this is a pretty neat idea, I like analytics and I'm sure much like myself, lots of people would be interested in seeing the analytics for the sites they visit. The issue here is that I've realised it probably doesn't look good for a site with my small amount traffic. To go back to my previous point, it wouldn't look good for the likes on all my articles to be in the 0-2 range. I'd rather not show these things and let an outside reader guess how much traffic I get (in most cases, it would probably be higher than what it actually is).

As for the article stats page, I'm just not even sure what I'm supposed to show. Most used tags? Highest number of swears? It seems a bit too novel for me.

#### Selenium tests

This is just testing but for the front-end rather than back-end. I may actually end up doing this, just to learn how.

#### Compress images better

This sort of goes with the web.dev point, but it's on it's own because it is actually pretty important. Currently, all the thumbnails for my articles are 1920x1080px images, which is awful for bandwidth. I really need to compress them, hopefully I will be bothered soon.

#### Get the fucking search working

I did this :) we can skip it.

#### Archive - pages by year

In the /archive page, I want to split the articles in pages, ordered by year. This should be done soon.

#### Edit articles in markdown instead of HTML

This would just make my workflow a whole lot simpler and faster, I have a few ideas to get this working and it opens a whole lot possibilities for future improvements. It's quite a bit of work, bit this is definitely going to be worked on next.

#### Move to docker container

Move to Docker container. Do I need to say anything else?

All right, that's all of them. Come back next year and we'll see how many I did (or didn't).
