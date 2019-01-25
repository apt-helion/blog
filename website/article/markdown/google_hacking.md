---
title: Google Hacking For Fun And For Profit
category: infosec
date: 2018-11-08
thumbnail: google-thumb.png
tags: google
description:
---

Google Hacking (or Google Dorks) can be very useful when gathering information on a business as it is essentially a way to use the search engine to pinpoint websites that have certain flaws, vulnerabilities, and sensitive information that can be taken advantage of. Google offers the opportunity to perform advanced search queries using special operators. Beyond the common operators (AND, OR, +, -, “”) there are more specific filters that you can use.

![image-alternative](/common/static/img/google-search.png)

If you constantly look up code error messages on Google like me, you've more than likely come across a Google Dork when clicking the *'more results from stackoverflow.com'* which changes the search term to this.

![image-alternative](/common/static/img/google-dork-search.png)

Basically it's just added site:stackoverflow.com to the search query which means that it will limit all the results to only those from the given website. There are far more operators, too many to include in this guide, but I'll go over some of the most common:

* **cache**: will show the cached content of the specific website.
* **link**: will display websites that have links to the specific website.
* **site**: limits the search results to the website given.
* **filetype**: searches for all documents with a specific extension.
* **ext**: very similar to filetype, but this looks for files based on their file extension.
* **intext**: searches the entire content of a given page for keywords supplied.
* **allintext**: similar to the previous operator, but requires a page to match all of the given keywords.

You can also prepend a hyphen to all of these (except cache) to exclude the filter instead. E.g `-site:www.site.com` will exclude all results from `site.com`.

Now let's look at another example. We will be looking for PDFs on the docker site by searching `site:www.docker.com filetype:pdf`.

![image-alternative](/common/static/img/google-docker.png)

When used correctly, Google Dorks can uncover some incredible information such as email addresses and lists, login credentials, sensitive files, website vulnerabilities, and even financial information (e.g. payment card data).

One Google Dork I particularly enjoy is `inurl:org AND filetype:sql AND intext:password`. I won't show you a picture of it in action (because it includes sensitive data), so you should just go and search it yourself. If you look long enough, you may find some very interesting results...

For more queries, you can look at the links below.

* [Exploit DB: GHDB](https://www.exploit-db.com/google-hacking-database/)
* [Google Dorking](http://www.google-dorking.com/)

