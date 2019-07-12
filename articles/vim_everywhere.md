---
title: Vim EVERYWHERE
category: miscellaneous
date: 2019-07-12
thumbnail: vim-e-thumb.png
tags: vim
description:
---

For the past week I've been trying make everything in my laptop work with
Vim key-bindings. So far I've gotten around 40% of what I use the most to work
with Vim key-bindings and today we'll go through each of them.

### Terminal

This is obviously the easiest so lets start here. Oh my Zsh has a [vi-mode][]
plugin that makes using the shell much easier. You can go into normal mode
by pressing `ESC` and from there you can use all the normal Vim keys to navigate.

For editing text, you can use Vim to get Vim bindings, shocking right?

For everything else, most TUIs like Weechat either have Vim bindings built in, or
have plugins for them.

[vi-mode]: https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins/vi-mode

### Finder

Finder has no options to change key-bindings, so you can just replace it
entirely with [ranger][] which is a terminal file manger with Vim bindings.
You're going to see me replace many GUI applications for TUI applications so
get used to it.

[ranger]: https://github.com/ranger/ranger

### Apple Mail

Here's another one that we replace with a TUI. There are many good mail
clients for the terminal, but one of my favourites is [aerc][] which as Vim
bindings build it. Unfortunately, I haven't managed to get Protonmail Bridge
to work with it, so I still need to use Apple Mail ;(

***Disclaimer:*** I'm a Patreon supporter for the aerc's author (Drew
DeVault).

[aerc]: https://git.sr.ht/~sircmpwn/aerc

### iTunes

There's a few options with this one. You can either use [ViTunes][] which is a
TUI, or you can use something like [itunes-cli][] which allows you to control
iTunes from the terminal. Personally, I use itunes-cli because I find it
easier.

[ViTunes]: https://github.com/ryanflannery/vitunes
[itunes-cli]: https://github.com/ktr0731/itunes-cli

### Firefox

There are quite a few Vim interfaces for Firefox, but the best (in my opinion)
is [tridactyl][]. It's incredibly powerful and comes with the ability to edit
it's configuration in a `tridactlyrc` (just like Vim!). You can peek at [my tridactylrc][]
for a look at some of the options.

[tridactyl]: https://github.com/tridactyl/tridactyl
[my tridactylrc]: https://github.com/beanpuppy/dotfiles/blob/master/tridactyl/tridactylrc

### Everything Else

There's an application called [vim-anywhere][] which opens up a vim buffer
whenever invoked. However, I find this a bit too cumbersome to use. Instead I
use [Karabiner-Elements][] which is a low level macOS kernel extension that
gives you a virtual keyboard you can heavily customize to your own liking.

Karabiner comes with a [vi-mode][] modification. Once you've added and enabled
it, you can "trigger" vi-mode by pressing simultaneously either the key `D` or
`S` and then `h/j/k/l` or `b/w` to move around text. You have to keep your
trigger key pressed while moving around. Same goes for visual mode but with
`V` as the trigger key. Don't forget to set the simultaneous threshold to
something between 200-300 for this to work better.

[vim-anywhere]: https://github.com/cknadler/vim-anywhere
[Karabiner-Elements]: https://github.com/tekezo/Karabiner-Elements
[vi-mode]: https://pqrs.org/osx/karabiner/complex_modifications/#vi_mode
