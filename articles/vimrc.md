---
title: Looking At My .Vimrc
category: miscellaneous
date: 2018-09-12
thumbnail: vimrc-thumb.png
tags: vim,vimrc
description:
---

This is a reference guide for my .vimrc that you can find [here](https://github.com/beanpuppy/dotfiles/blob/master/vimrc). This is mainly being written because I keep forgetting what keybindings some of the plugins use. Even though this is not a guide to the .vimrc, if you use Vim you may still find this somewhat useful. If you don't use Vim, you are a bad person and should go away >:(

### Leader

The leader key has been remapped to the comma key `,`.

### Tabs/Buffers

Move between tabs with `--` to go back and `==` to go forward.

Move between buffers with `TAB-k` to go back and `TAB-j` to forward.

Close buffers with `LEADER-bq`.

### Windows

Move between window panes with `CTRL-[h,j,k,l]`.

Create a terminal window (only on Vim8) with `LEADER-ht` for horizontal and `LEADER-vt` for vertical.

Close a terminal window with `ESC`.

### Commands/Other

Show the weather (for Sydney) with `LEADER-we`.

Reference the current file's path in command line with `%%`.

Run the current file with Python with `:Pyrun`. Do it with interactive mode `:PyrunI`.

Write as root with sudo tee hack with `:w!!`.

Rename current file with `LEADER-rn`.

### Plugins

#### [Undotree](https://github.com/mbbill/undotree)

Open undotree with `LEADER-u`.

#### [TagBar](https://github.com/majutsushi/tagbar) / CTags

Open TagBar with `LEADER-t`.

#### [Easymotion](https://github.com/easymotion/vim-easymotion)

Trigger word motion with LEADER LEADER w.

Search ctags with LEADER-..

#### [Multiple Cursors](https://github.com/terryma/vim-multiple-cursors)

Taken from the docs (mostly), I haven't played around with this very much:

* start: `CTRL-n` start multicursor and add a virtual cursor + selection on the match
+ next: `CTRL-n` add a new virtual cursor + selection on the next match
+ skip: `CTRL-x` skip the next match
* select all: `ALT-n` star muticursor and directly select all matches
You can now change the virtual cursors + selection with visual mode commands. For instance: c, s, I, A work without any issues. You could also go to normal mode by pressing v and use normal commands there.

At any time, you can press `ESC` to exit back to regular Vim.

#### [Commentary](https://github.com/tpope/vim-commentary)

Comment out one line with `gcc`.

Comment out multiple lines (in visual. mode) with `gc`.

#### [Surround](https://github.com/tpope/vim-surround)

Change the surrounding elements of a word with `cs/old/new/`. e.g `cs'"`.

Wrap a word with elements with `ysiw/elem/.` e.g `ysiw{`.

#### [Easymotion](https://github.com/easymotion/vim-easymotion)

Trigger word motion with `LEADER-LEADER-w`.

