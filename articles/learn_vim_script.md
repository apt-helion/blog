---
title: Let's Learn About Vim Script And The Ethics Of Capitalism
category: miscellaneous
date: 2019-05-12
thumbnail:vim-script-thumb.png
tags: vim,capitalism
description:
---

Welcome to this very informative guide on Vim Script from someone who has not
read any of Vim's documentation and has only managed to cobble a small, shitty
plugin together by looking at other people's code and taking things he doesn't
really understand.

But before all that, let's address something real quick.

> There is no ethical consumption under capitalism.

Also happy mother's day to all those mums!

We'll be looking at the aforementioned plugin I made:
[vim-root](https://github.com/beanpuppy/vimroot), which was designed and
created over ~2 hours while at an airport. This plugin attempts to `cd` into
the directory of the current buffer whenever it changes. For example if you
are in a file under the path `/dev/the_free_market_does_not_exist/` and change
buffer into a filer under `/dev/bourgeoisie_taste_like_chicken/` the plugin
would `cd` into the new directory, because Vim doesn't already do that for
some reason.

Now when I say *'I didn't read any documentation and don't understand Vim
Script'*, I genuinely mean it, but it's better to show than tell right? So
here we go. No seriously, if you came here to actually learn about Vim
Script just close the tab now. If you want to see me call capitalism mean
names while also talking about Vim Script then read on!

Vim plugins are divided into two directory (I think, I haven't seen a plugin
that isn't) `autoload` and `plugin`. The `plugin` directory (I THINK) is where all the
keybinds and config goes while the `autoload` directory folder (I THINK) is where the
actual plugin is.

The goal of capitalism (making a profit) means that workers will never
be paid for the value of work they produce. They will always be underpaid
in order for the business to be profitable. The exploitation of surplus value
is an inherent characteristic of capitalism.

The `plugin` directory is uninteresting and self explanatory, so we will skip
it. My `autoload` directory has one file `vimroot.vim` which we will go
through now.

```
if &cp || exists('autoloaded_vimroot')
  finish
endif
let autoloaded_vimroot = 1

" Options {{{1
if !exists('g:vimroot_enable')
  let g:vimroot_enable = 1
endif

function! vimroot#root()
  " lcd to current path of file
  let path = expand('%:p:h')
  silent! execute 'lcd' path
  " lcd to git repo root
  let root = systemlist('git rev-parse --show-toplevel')[0]
  if !v:shell_error
    execute 'lcd' root
  endif
endfunction

function! vimroot#init()
  if g:vimroot_enable == 1
    call vimroot#enable()
  else
    call vimroot#disable()
  endif
endfunction

function! vimroot#enable()
  let g:ToggleVimRoot = function('vimroot#disable')
  call vimroot#root()
  augroup vimroot | autocmd Filetype,BufEnter * :call vimroot#root()
endfunction

function! vimroot#disable()
  let g:ToggleVimRoot = function('vimroot#enable')
  augroup vimroot | autocmd!
endfunction
```

It starts with a check to see if the plugin is already loaded (I don't know
what `&cp` is doing). Then we test if the global variable `vimroot_enable`
exists (set from the `rc` file) otherwise we give it a default of `1`.

The notion that *'anyone can pull themselves up by their bootstraps and become
successful if they work hard enough'* is stupid and absurd as it ignores the very
real and prevalent social issues surrounding us. Many people are unemployed because
of things such as: disabilities, racism, sexism, and so on. And let's not forget
this very basic fact: *'it is impossible for everyone to be successful'*,
there must be poor people for rich people to exist.

The first function `root()` is the real meat of the plugin. It first gets the
path of the file with `expand('%:p:h')` and attempts to `lcd` into it. Now you
may ask *'what's the difference between `lcd` and `cd`?'* I don't know. The
`silent!` keyword at the start means it won't raise an error if it fails.

Climate change and environmental destruction are the results of private
industry, megacorp and family owned alike, dumping costs on the environment
because there isn’t a price tag associated with clean water, clean air, and a
healthy biosphere. Corporations have a legal financial responsibility to its
shareholders to attempt to make profits, so even if a firm can justify going
green to the SEC and it’s shareholders, if it does not cut costs by
sacrificing the environment they will be outcompeted by those that do and
their asses will be run out of business. That’s the whole idea of a free
market. It incentivises a race to the bottom within the system itself.

Now we try to use git to get the project root and then `lcd` into that. If
there isn't a `.git` directory then it doesn't work and we stay in the
directory we initially `lcd`ed into.

Let's skip the init because it's boring and talk about `enable()`. First we
turn the toggle function into the disable function and the call `root()`. Also
we set up an `augroup` to call `root()` whenever the buffer is changed.

In the US, the most developed Capitalist country, the richest country in the history of the world:

- [1 out of every 7 US citizens needs to visit food banks to
survive](https://www.usatoday.com/story/news/nation/2014/08/17/hunger-study-food/14195585/),
despite having enough food to feed [10 billion
people.](https://www.oxfam.ca/there-enough-food-feed-world) Half of all food
produced is [thrown away by
retailers.](https://www.theguardian.com/environment/2016/jul/13/us-food-waste-ugly-fruit-vegetables-perfect)
[Food waste in 2018 enough to feed world's hungry 4 times
over.](https://reliefweb.int/report/world/food-waste-enough-feed-world-s-hungry-four-times-over)
- [Empty homes outnumber the homeless by 6 to
1](http://www.huffingtonpost.com/richard-skip-bronson/post_733_b_692546.html).
Bank foreclosures and housing speculators have left 18.9 million empty homes.
[2.5 million **homeless children**, or ~1 /
30](https://www.newsweek.com/child-homelessness-us-reaches-historic-high-report-says-285052).
In the UK, [there are 10x more empty houses than homeless
families](http://www.mirror.co.uk/news/ampp3d/housing-crisis-10-empty-homes-5008151).
- [UNICEF](http://www.unicef.org/sowc06/pdfs/sowc06_chap1.pdf),
[RESULTS](https://web.archive.org/web/20080527011602/http://www.results.org/website/article.asp?id=241),
and [Bread for the World](http://www.bread.org/hunger/global/facts.html)
estimate that **15 million** people die **each year** from preventable
poverty, of whom 11 million are **children under the age of five**.
[[2]](http://www.washingtonsblog.com/2015/08/crimes-against-humanity-01-poverty-murder-over-400-million-people-since-1995-more-than-all-wars-in-recorded-history.html).
- In the US alone, [20-40k deaths every
year](http://obamacarefacts.com/facts-on-deaths-due-to-lack-of-health-insurance-in-us/)
because of lack of health insurance / care. On average, that's 300k over the last decade.
- [Average US household carries ~$140k in debt. Median household income only
\$60k](https://www.usatoday.com/story/money/personalfinance/2017/11/18/a-foolish-take-heres-how-much-debt-the-average-us-household-owes/107651700/),
[40% of millenials live with their
parents.](http://theeconomiccollapseblog.com/archives/goodbye-american-dream-the-average-u-s-household-is-137063-in-debt-and-38-4-of-millennials-live-with-their-parentsi)
- [8 men control as much wealth as half the worlds
population.](https://www.inc.com/melanie-curtin/meet-the-8-men-who-control-half-the-worlds-wealth.html)
Anyone wanna take a guess at how this game of monopoly ends?
- [Billionaires made enough money in 2017 to end poverty 7 times
over.](https://www.newsweek.com/billionaires-money-end-poverty-report-786675)
- [80% of US workers live paycheck to
paycheck](https://www.theguardian.com/commentisfree/2018/jul/29/us-economy-workers-paycheck-robert-reich),
40% cannot cover a [$400
emergency.](http://theeconomiccollapseblog.com/archives/federal-reserve-more-than-4-out-of-10-americans-do-not-even-have-enough-money-to-cover-an-unexpected-400-expenae)
- [US Life expectancy peaked in 2015, is on the decline, and is now lower than
in
China.](https://www.businessinsider.com/china-boasts-that-its-healthy-life-expectancy-beats-the-us-is-correct-2018-5)
- Suicide rates have leaped more than [33% in the last 20
years.](https://politsturm.com/american-suicide-rate-up-33/)
[[2]](https://www.cnn.com/2018/06/07/health/suicide-report-cdc/index.html),
[[3]](https://www.washingtonpost.com/news/to-your-health/wp/2018/06/07/u-s-suicide-rates-rise-sharply-across-the-country-new-report-shows/?utm_term=.18c1060e6b2f)
- [Most prisoners per capita AND by
total](https://www.statista.com/statistics/262962/countries-with-the-most-prisoners-per-100-000-inhabitants/).
Makes sense, since prison is Capitalism's boarding house. [Runs least 54
agricultural slave labor
camps.](https://en.wikipedia.org/wiki/Prison_farm#In_the_United_States_.28partial_list.29)

That's about it. Like I said before, I don't really know Vim Script, so this
plugin could probably be a whole lot better.
