---
title: Saving The World One Dark Mode Setting At A Time
category: development
date: 2018-12-03
thumbnail: dark-mode-thumb.png
tags: blogpost,javascript
description:
---

According to very reputable [sources](https://en.wikipedia.org/wiki/List_of_sauces), light mode displays in software are actually the leading cause in climate change. It has also been proven that people who use light mode have a much lower IQ because the brightness of the screen burns their brain cells away and that's how science works I think. If you disagree with this, you are cyber bullying me and I will report you to ASIO.

Anyway, now you must be wondering why my blog looks like this.

![image-alternative](/article/static/img/dark-mode-no.png)

And that's because I haven't been bothered to change any of the CSS from the Bootstrap template I bought.

But I've decided that I've had enough! I've gotten off my lazy ass and immediately sat back down (because who codes standing up?) to spends HOURS to add a dark mode to this website for you, my dear reader!

Now your eyes will be saved from the global warming, IQ destroying tyranny of light modes by just pressing the Dark Mode button at the bottom of the page.

![image-alternative](/article/static/img/dark-mode-button.png)

Now look at it... beautiful.

![image-alternative](/article/static/img/dark-mode-yes.png)

And in case you wanted it. Here's the code.

```javascript
if( theme === "dark" ) {
    $("head").append('<link rel="stylesheet" href="/common/static/css/dark-override.css">');
    $('#ToggleTheme').text('Light Mode');
}

$('#ToggleTheme').click(function() {
    if( theme !== "dark" ) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }

    location.reload();
});
```
