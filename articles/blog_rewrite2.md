---
title: Yet Another Blog Rewrite
category: development
date: 2019-08-27
thumbnail: rewrite2-thumb.png
tags: blogpost
description:
---

Do you remember [seven months ago](/article/blog2_release) when I said
development of this blog was finished and I was just going to make small
changes from now on? Turns out that was a hecking lie.

I've been very bored the last few weeks, so I've decided that I want rewrite
this site in an entirely different technology stack. I've had a bit of
deliberation on what the new stack will be but the basic jist of things that
are changing is this:

* Svelte + NodeJS instead of jQuery + Python for client/server side code.
* Redis instead of MariaDB for storing emails and caching articles.
* Dokku for deployment instead of a bunch of garbage Shell scripts.
* Images are going to go through a CDN instead of me serving them myself.

#### Why are you using a JS framework?

Yes, a static site generator like Hugo or Jekyll would probably work better
and be much more performant. But that crap is boring and I like
over-engineering things.

#### Why Svelte instead of React or Vue?

React sucks big ween and I can't be bothered to learn Vue. And to be honest,
Vue is probably garbage as well.

I was going to wait until Svelte had TypeScript support before doing this, but
then I remembered that I don't actually care about TypeScript.

#### You should write it in Rust instead

That is a very good idea and I was almost going to do it until I found out
that there are no good Markdown to HTML crates and I don't want to write my
own. Maybe I'll do it on the next rewrite.

#### What's your favourite ice cream flavour?

Stick to questions about the topic at hand please.

#### What's wrong with MariaDB?

I really don't need a relational database for this stuff and I hate
configuring the `my.cnf` file.

#### Why were you using a bunch of garbage Shell scripts in the first place?

I've never claimed to be smart.

#### What's up with the triangle?

I don't know what to draw and it was the first shape that came into mind.

#### When will this be done?

I have no idea.
