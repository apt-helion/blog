---
title: Spotify Playlist Depression Score
category: development
date: 2018-06-15
thumbnail: spds-thumb.png
tags: spds,python,flask
description:
---

**Update 2019-01-25:** This is no logner online, I'm too lazy to maintain it, but you can still look at it on GitHub.

[Spotify Playlist Depression Score](https://playlistdepressionscore.com) is a web application I built to determine how depressing a playlist is from it's songs. This article explains how I built it and how it works. As of writing, SPDS is on it's 1.0 release, so keep in mind that there are a lot of improvement to be made, and that this article may not always be up to date. To view the most up to date changes, go through the [changelog on GitHub](https://github.com/beanpuppy/spds/releases) or view all SPDS articles through the [#SPDS tag.](/tag/spds)

#### Table of Contents

* [The Architecture](#0x100-the-architecture)
* [The Logic](#0x200-the-logic)

### 0x100: The Architecture

A big change from the development of this blog is the use of Flask as the web framework. This decision was almost entirely made by the fact that I had no idea how to use sessions in Simplerr at that time (although as it turns out they are functionally the same). This wasn't detrimental in any way, but if I was bothered to redo the application I wouldn't be using Flask.

The application heavily relies on AngularJS, which was a real walk into the unknown for me. I've never done much high level front end development, but making a smooth user experience was a must for this project. Angular just does an AJAX call on a Flask endpoint and displays it when it is received. This seems like a small thing, but it allows me to have a proper loading screen and display much more information to the user. Overall I'd say it looks pretty nice, although I can't say the same for the code.

### 0x200: The Logic

If you are looking here to find some incredibly advanced mathematics and natural language processing to see how to determine depression, I'm sorry but you're going to be very disappointed. While I do one day hope to be able to make it more advanced (and useful), this project was more of a learning exercise for a few technologies, and as such, the code behind it is quite simple.

The reason it's the '**Spotify** Playlist Depression Score' instead of just 'Playlist Depression Score' is because the Spotify API is an easy way to make sure I can find every song in the playlist. Spotify also does an audio analysis on every track they have. Included with this is a field called 'valence', which measures from 1 to 0 how happy the audio for the track is, where 1 is MAXIMUM HAPPY and 0 is depression. This means that half our job is already done for us! YAY! Now all that's left is the lyrics.

Unfortunately Spotify left us the hardest part of calculating depression. While audio sadness can be somewhat easily determined by looking a what chords are being played, the lyrics are much more difficult as we would need to know what the entire song 'means'. The application would need to be able to understand what the words mean and what they mean when they are sung together. This is much too hard for me so I took the easy way out.

First we use the Genius API to get our lyrics. However, for some reason getting a track from the API won't give us the lyrics, so instead we use the API to find the URL to the Genius website where we can scrape the lyrics from (luckily they are all under a CSS class called 'lyrics' which makes it very easy to find with BeautifulSoup). Now we go through the song word by word picking out sad words and adding them to a score. I just took this [lexicon](https://github.com/motazsaad/emotion-lexicon) and used the emotions most commonly associated with depression. In order to get the valence to match the 1 to 0 scale of Spotify's audio, we find the percentage of sad words to lyrics and find the lyrical density of the song to find how important the lyrics are to the song. Then we do some maths which to be honest I've sort of forgotten what it was doing (because it was mainly trial and error to find a value I thought looked right. Impressive, I know). Now we can just average it with the audio valence, and we've found our score!

Of course I could sit here and contemplate typing a single sentence for several hours and generally being incredibly unsure of what I should be saying, but it would probably be better to just show the code as it would do a better job explaining what it does than I would.

```python
    audio           = spotify.get_audio_features(track['track']['id'])
    audio_valence   = audio['valence']
    lyrical_valence = 0.9 if audio_valence > 0.3 else 0.9 - audio\_valence
    score           = round(audio_valence * 100)

    incomplete = 'yes'

    if 'error' not in lyrics:
        words = re.split(r'[\s\]\[]', lyrics)
        sad_words = 0
        for word in words:
            if word in Config.STOP_WORDS or word == '':
                words.remove(word)
            if word in Config.LEXICON_SADNESS:
                sad_words += 5
            if word in Config.LEXICON_FEAR:
                sad_words += 2.5
            if word in Config.LEXICON_ANGER:
                sad_words += 1

            percent_sad = sad_words / len(words) * 100
            lyrical_density = len(words) / track['track']['duration_ms'] * 1000
            lyrical_valence = ((1 - (percent_sad * (1 + lyrical_density)) + 100) / 100)
            incomplete = 'no'

    score = round((audio\_valence + lyrical\_valence) / 2 * 100)
```

As you may have noticed, the `incomplete` flag was made because Genius doesn't always have the lyrics for a song so we have to guess how sad it's lyrics are (if it even has them). This is just based on the audio valence, because I like to assume sad instrumentals means sad song.

That's the entire application, it's very small and I have a few more ideas that will probably never get implemented. But it did it's job in allowing me to learn some new stuff, and that's all that matters right?
