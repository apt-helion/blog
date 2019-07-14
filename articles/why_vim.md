---
title: Why Vim?
category: miscellaneous
date: 2019-07-14
thumbnail: why-vim-thumb.png
tags: vim, lingustics
description:
---

I've talked about Vim a lot in this blog. It's obvious that I'm quite a fan on
Vim, you could even call me a fan-boy, I would too! But I've never
addressed why I use Vim. [This post by Jon Beltran de
Heredia](http://www.viemu.com/a-why-vi-vim.html) goes over some of the more
common points of why Vim is so widely used by correcting various
misconceptions about the editor. It's a great post and I highly recommend
reading it, but I'm going to tackle the question at a slightly different angle.

Think back to LING111, your first uni course about linguistics. Do you
remember what the lecturer was telling you? No? That's fine, I'll give you an
excerpt from my textbook.

*"Knowledge of a language enables you to combine sounds to form words, words to
from phrases, and phrases to form sentences. You cannot buy a dictionary or
phrase book of any language with all the sentences of the language ... because
the number of sentences in language is infinite. Knowing a language means
being able to produce and understand new sentences never spoken before. This
is the **creative aspect** of language."*[^1]

Remember now? The **creative aspect** of human language is one the most
important factors that distinguish our language from animal "language" (the
other factor being displacement, but let's not get into that now). While
most animals have some form of communication, none (as far as we know) possess
this creative aspect.

Let's look at birds as an example. Birds communicate through bird songs and
annoying screeching at 5 am, but there is no evidence of any internal messages
to these songs; they cannot be segmented into discrete meaningful parts and
rearranged to encode different messages as can the words, phrases, and
sentences of human language.

I hope you can see where I'm going with this. But if you don't know any Vim or
are just plain dumb, I'll spell it out for you:

```
Vim == Human language
Every other text editor/IDE == Annoying bird language
```

Here's an example from the article I mentioned above.

*"Commands in vi/vim are meant to be combined - 'd' means delete, 'e' means
'move to end of word', then 'de' is a complete command that deletes to the end
of the current word (something like Ctrl-Shift-Right, Left, Del in most
regular editors)."*[^2]

This is the power of Vim. The ability to mix commands as if they were the
words to a sentences of a language. It's helped even further by how many of
these keys can be remembered by mnemonics. You've seen `d` for delete and `e`
for end, but there's also `w` for word, so you can do `daw` for delete a word.
Instead of `d` you can use `y` for yank (copy) where `ye` yanks from the
cursor to the end of a word and `yaw` yanks the word under the cursor.

In contrast, look at this keyboard shortcut cheat sheet for VS Code:

![image-alternative](/website/article/static/img/vscode-keys.png)

This is all there is. The entire dictionary of VS Code. Every sentence that
could possibly said is right here (unless you install some more plugins, like
a Vim emulator per se... but more on that later).

Now that that's all been said, I hope you'll think what I'm going to say
next to be pretty reasonable.

> The reason I use Vim is because it feels like an extension of myself.

If you're a manual transmission elitist (which I also am), you'll probably
understand. Driving an automatic feels wrong, like you're not actually in
control of the car. Sure it's probably a lot easier, your legs won't die
whenever you hit heavy traffic, and there's much less to think about. But it
*feels* wrong.

To beat this metaphor a bit more, using a Vim emulator feels like driving a
car with a crappy manual transmission. I can *feel* that this stick shift isn't
directly connected to the gearbox, it's soft and mushy, just like how using
the Vim plugin for VS Code feels bloated because... well, because it is
bloated.

It may be that my MacBook is too slow for a goddamn text editor, but every
attempt I've had to use VS Code always ends up with me quitting after a day.
Setting up VS Code with a Vim emulator seems like a win-win, does it not? You
get that beautiful Vim language of commands with all the features of a
semi-IDE!

But no, that 2 second start time *feels* like a week when compared to the near
instant Vim. My workflow is constantly interrupted with the fact that I still
actually can't use Vim's language to do basic things like change my
preferences or use the file manager, and have to either resort to:

1. Using the mouse or
2. Learning the garbage dictionary of hotkeys I showed before.

It's not just VS Code, I actually prefer it to many other IDEs because it's
not really an IDE, and thus, not as bloated as other IDEs. The Vim emulation
is slow and a bit clunky, yes, but at least it exists. I only give it so much
clout because it's the other editor I use on a somewhat regular basis.

No editor/IDE has managed to drag me away from Vim, I don't think there's any
feature of an IDE that I could supplement in Vim, although SwiftUI with Xcode
is looking to be particularly juicy - if something like that was developed for
the web it might do it. But even with that, Vim would still remain king in my
favourite programming domain: systems programming, where there ain't no UI.

So that's it then. If you've never tried Vim I seriously recommend giving it
a go. The learning curve is steep I know, but if you can remember a few
commands a day, you'll be stringing complicated sentences in no time.

[^1]: Fromkin, Rodman, and Hyams 2013 An Introduction to Language, 10th edn, International Edition, Cengage Learning Inc, Florence, United States
[^2]: Beltran de Heredia, J 2007, Why, oh WHY, do those #?@! nutheads use vi?
