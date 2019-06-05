---
title: Pixel Sorting And Hiding Your Face From Strangers On The Internet
category: miscellaneous
date: 2019-03-19
thumbnail: pixel-sort-thumb.webp
tags: processing
description:
---

Pixel sorting is an interesting effect used to make forms of glitch art. It is
the process of isolating a horizontal or vertical line of pixels in an image
and sorting their positions based on any number of criteria. For instance
pixels positions may be sorted by each pixel’s luminosity, hue or saturation.
While some glitch art, such as opening the image in a hex editor and changing
a bunch of shit can be done manually by hand, pixel sorting would be very time
consuming, and thus is mainly done using a script.

There are many scripts to create this effect like [this one in
Python](https://github.com/satyarth/pixelsort/), but we are going to use
[this popular script](https://github.com/kimasendorf/ASDFPixelSort) in
Processing written by Kim Asendorf, the artist who popularised pixel sorting.

But what image should we use to sort? If you've read the title you should
already know - we're going to sort a picture of me! Now as far as I know there
are only ~2 images of me on the internet (that I know of), although none from the past 5 years.
One is from when I was 10 and took a selfie on an old Facebook profile I don't
know how to delete and the other ones are probably from group pictures in
high school.

I'm going to pixel sort this somewhat recent image to use for my
[Instagram](https://www.instagram.com/beanpup.py/) which you should all follow
if you want to see pictures of garbage on your timeline.

![image-alternative](/website/article/static/img/pixel-no.webp)

Okay let's finally start.

Our particular script loops through both the columns and the rows of the
image, but it doesn’t pixel sort the entire column or row, if it did, the
result would look more like a blank gradient than anything interesting.
Instead for each column and row it looks for a pixel to start sorting on and
then it looks for a pixel to stop sorting on — this makes the algorithm
somewhat intelligent resulting in identifiable elements of the image being
left untouched.

In order to decide which pixel to start sorting on and which to stop sorting
on this script can operate in three different modes. The mode can be changed
by adjusting the mode variable, by default it is set to 1, but can be changed
to either 0 or 2 as well. Different modes will work better depending on the image itself.

In mode `0`, or black mode, the script will begin sorting when it finds a pixel
which is not black in the column or row, and will stop sorting when it finds a black
pixel. The script identifies black pixels by comparing the pixel’s color value
to a threshold, if it’s lower than the black threshold the pixel is deemed to not
be black, if it’s higher it’s deemed to be black. You can adjust this threshold by
changing the `blackValue` variable which is by default set to `-16000000`.

This goes for the rest of the modes too. Mode `1` is brightness mode which
starts when it finds a bright pixel and stops when it finds a dark one. While
mode `2`, white mode is the opposite of mode `0`. These can also be
adjusted by changing their corresponding variables - `brightnessValue` and
`whiteValue`.

We will be using mode `1` because the image is pretty bright. Here's the first
run.

![image-alternative](/website/article/static/img/pixel-1.webp)

A bit too much sorting, although it does hide my face quite well so that's
pretty close to a win!

Let's change the `brightnessValue` from `60` to `50`.

![image-alternative](/website/article/static/img/pixel-2.webp)

And that made it worse, okay how about `70`?

![image-alternative](/website/article/static/img/pixel-3.webp)

Good enough! Normally I would work on this a bit more and slowly change
stuff until it's close to perfect but unfortunately for me, I have crippling
anxiety and can't look at a picture of myself for too long without becoming
incredibly uncomfortable.

If your interested in this, you should try it yourself. If you don't want to
download Processing, you can use the Python script I mentioned above, although
I've never used it so I can't say if it's good.
