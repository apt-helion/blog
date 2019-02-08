---
title: A Basic Pen Test Of Every Web Application I've Made
category: infosec
date: 2018-09-06
thumbnail: wapt-thumb.png
tags: pentest,python,spds,viperidae,blogpost
description:
---

This is going to be a very short penetration test mainly focusing on low hanging fruit, mostly because I don't care very much for what I've made - they were all created to serve a specific goal of allowing me to learn something new instead of actually being useful. In fact, this blog is the only thing I still maintain and all the others will probably be turned off at some point and to be honest, I seriously doubt I will find any exploits. While security wasn't a main focus when creating these applications, I believe (or at least I hope) I wasn't stupid enough to leave myself vulnerable to any of the basic exploits I will attempt here today. Although there is only one way to find out, so let's get on with it.

#### Table of Contents

* [SPDS](#)
* [Viperidae](#)
* [Blog](#)

### 0x100: SPDS

[Spotfiy Playlist Depression Score (SPDS)](/article/spds_release) is an application that rates how depressing your Spotify playlist is. This was my first foray into the JavaScript framework world with AngularJS, so let's start off with some basic XSS.

The only field we can enter any inputs is this one here, where you can manually enter a playlist.

![image-alternative](/article/static/img/wapt-spds-xss-find.png)

So now let's inject some HTML code, I will try a `<h1>This shouldn't work</h1>`. It now displays this:

![image-alternative](/article/static/img/wapt-spds-xss-attempt.png)

Obviously, it didn't work because the playlist ID is never actually shown anywhere after you enter it (apart from the URL) and it is only used for the Spotify API. Entering a wrong ID will just to just not show anything, although it is only just now occurring to me that I should have implemented some sort of error message when you enter an ID that doesn't exist.

Next we could attempt a SQL inject. I know that the playlist ID given in the URL attempts a SQL query for a playlist in the database which acts as a cache for the Spotify and Genius APIs in order to prevent them from being called very often and speed up the process on subsequent ranking attempts.

Fortunately (or unfortunately, depending on whose side you're on), we won't even need to attempt it as [this code here](https://github.com/beanpuppy/spds/blob/master/app.py#L121-L125) shows that we still call the Spotify API to verify that it is an existing playlist ID before we even start our SQL query.

```python
playlist_id = request.args.get('playlist')
page        = request.args.get('page')
playlist    = spotify.get_playlist(user.get('id', 'me'), playlist_id, auth_header)

if not valid_token(playlist): return redirect('/search', code=302)
```

Okay then. What else can we do... session hijacking? We can log into Spotify which gives us an auth header, allowing SPDS to see user data (our playlists), the app then stores the auth header in the session to post to Spotify in future requests.

The web framework we're using (Flask), stores a session identifier in a cookie like so:

![image-alternative](/article/static/img/wapt-spds-session.png)

So if we manage to steal a victim's session, we will be logged into the victim's Spotify for our app! And this is where our pen test for SPDS ends. As far as I know, there is no way to get a session without having direct access to a victim's computer or the server hosting the app (or having it shown in a screenshot from a blog ;). Common ways like XSS won't work (as seen above) and packet sniffing won't work as everything goes through HTTPS while attempting to use HTTP instead will just redirect to this blog (for some reason. I should probably go fix that).

### 0x200: Viperidae

Okay so far the score is [Me (pen tester): 0 - Me (software developer): 1] and with Viperidae, my incomplete attempt at a search engine, it looks like 'Me (software developer)' is going for a commanding 0-2 victory.

Viperidae was supposed to have two parts to it's API, the main part being one used by developers. The developer part would allow devs to crawl and index their own sites and implement a search for them, allowing developers to easily implement a search for their own site by just hooking into the Viperidae API. Anyway the point is that most of this is not complete, and only a public facing site is active right now, which is very limited.

This is going to be a very quick test since the app is so small. In fact I can sum it up in bullet points.

* **XSS:** No. The JS framework I was learning this time (React) sanitises everything.
* **SQLi:** No. It doesn't use SQL (the public version doesn't, the developer version would).
* **Session Hijacking:** No. It doesn't use sessions.

However, there is one part I been concerned about for a while and just haven't been bothered to check if it was actually a concern. If you look at the code for the crawler you will see [these three lines](https://github.com/beanpuppy/viperidae/blob/canary/api/crawl.py#L202-L204).

```python
del(Spider.cache) # I'm pretty sure Spider.cache causes a memory leak
gc.collect() # so this just makes sure it is cleared, we don't need it anymore
Spider.cache = {} # I actually have no idea, should probably test it
```

As you can see from the comments, I am concerned about the cache causing a memory leak, as the crawler saves every page it requests into this cache. Since Spider.cache is a class attribute, it is shared between all instances of classes. I was unsure if this was ever cleared so I manually did it myself. Now I am finally going to test this.

We will do two tests - one with the *'fix'* and one without. I will be using the script below which requests several sites for the API to index and then monitor the memory usage.

```python
import requests

URL = 'https://viperidae.app/index'

SITES = [
    'https://blog.justinduch.com',
    'http://www.zachtronics.com',
    'https://www.redpandanetwork.org',
    'https://infosecjon.com',
    'https://www.malwarebytes.com',
    'https://www.docker.com',
    'https://www.bleepingcomputer.com',
    'https://www.renaultsport.com',
    'https://frog.com',
    'https://www.bookdepository.com'
    'https://plenz.com'
]

def test_memory():
    for site in SITES:
        print(f'Requesting {site}')
        payload = { 'u' : site }
        requests.get(URL, params=payload)

if __name__ == '__main__':
    test_memory()
```

Here is the memory usage before we start.

![image-alternative](/article/static/img/wapt-viperidae-memory.png)

Now we will run the script with the *'fix'* implemented.

There was no difference, the graph is exactly the same. I even looked at the memory usage from the server itself with free -m before and after, and also found no difference. So maybe the fix really is a fix? Okay so now let's remove it and run the test again.

![image-alternative](/article/static/img/wapt-viperidae-memory-after.png)

Again no difference except from a small decrease, which is probably just from me restarting the app. Now it is possible that I just didn't request as many sites as I may have should, but I would still have expected even the slightest increase in memory usage. So it turns out my fears of a memory leak were wrong and the fix was unneeded.

### 0x300: Blog

Considering this is the only web app I still maintain, I'm going to put a little more effort in trying to find vulnerabilities. However, we still have to start with the basics.

* **XSS:** No. There is nowhere to do it (the search bar doesn't work).
* **SQLi** No. The article IDs in the URL are actually used in a SQL query, but those are sanitised by peewee.
* **Session Hijacking:** No. There are no sessions being used.

With those out of the way, let's look at 'path file traversal'. If you look at the URLs for any of the images shown here, you will see that they are all from `/article/static/img/` which is the real path from the file structure of the app. The web framework I use is very determent on directory structure to act as individual pages. Looking at the code, we can see that the framework just serves the file by the filename straight from the specified directory without doing anything to it.

```python
@web('/common/static/', file=True)
def files(request, file):
	return './common/static/' + file
```

Let's attempt a dot-dot-slash attack by prefacing the sequence with `../.` With this, it may be possible to access directories that are hierarchically higher than the one from which we are picking the file. Let's attempt to show `/etc/passwd`.

Looking back at the code and it's directory structure, we can see that `/common/static/` is 4 directories down from the blog's root directory. Now we can assume (although I know it is) that the blog is hosted in `/var/www/` which is another 2 directories from root. In order to get to /etc/passwd, we will need to preface it with 6 `../`s. So it will look something like this:

![image-alternative](/article/static/img/wapt-blog-file-test.png)

If you try it yourself, you will just see that it resolves to `blog.justinduch.com/etc/passwd` and returns a 404. I also did another test where I attempted to get a file just outside in the `common/` directory, but that didn't work too.

Finally, let's attempt to get into to `/admin` page, which is where all the articles are edited. Currently what I do to add/edit articles is: turn on a dev instance of the app, go to `/admin`, add/edit the article, dump the SQL db to a file, and then source the file in the production server. What allows the app to determine whether it is either in a dev or production instance is a single environment variable. If we were somehow able to change the environment variable in our production server everyone would be granted access to `/admin`! Obviously this is not the best way of editing posts, but I do intend to change this... eventually.

The only problem is that I have no knowledge of environment variable exploits from a web app, but since this is the grand finale, let's do something I've not done so far but probably should have many times. I'm going to ~~Google~~ DuckDuckGo it.

![image-alternative](/article/static/img/wapt-blog-duck.png)

I didn't find anything. Not saying an exploit like that doesn't exist, just that I couldn't find anything like it. Either way, I really need to update this blog.
