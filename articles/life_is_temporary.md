---
title: Life Is Temporary And So Are Hard Drives
category: miscellaneous
date: 2019-02-08
thumbnail: harddrive-thumb.png
tags: backups,macos
description:
---

Last week I was messing around with my [dotfiles](https://github.com/beanpuppy/dotfiles), and long story short - I `rm -rf`'ed my home directory. So today, we're going to look at backup solutions.

### MacOS Time Machine
Let's start at the most obvious one and one that I was actually using: `Time Machine`.

This is a built-in backup feature for Macs. It creates incremental backups of files to an AirPort Time Capsule, a Wi-Fi router with built-in hard disk, or an internal/external disk drive. Time Machine saves hourly backups for the past 24 hours, daily backups for the past month, and weekly backups for everything older than a month until the volume runs out of space. At that point, Time Machine deletes the oldest weekly backup.

This is pretty great, because it meant I didn't lose anything except the last day of work which wasn't it the backup. But it wasn't pretty great. I soon found out two things: [Schrödinger’s Backup](https://www.novastor.com/schrodingers-backup-good-bad-backup/) applies to even the hard drive I kept Time Machine on and that life is a bitch.

The five most recent backups didn't work, and at that point I decided it would be better to just re-install MacOS. Thankfully, after the re-install I was still able to recover some files from Time Machine and the others were recovered in the next part.

### Online Backups
I've had [Backblaze](https://www.backblaze.com/) on my Mac since the day I bought it (this was before I knew Time Machine was a thing), and while it became somewhat unneeded (because of Time Machine) I still kept it for some reason. Backblaze and I assume other cloud backups solutions (I literally only know Backblaze, I guess that's marketing for ya), upload your files to the cloud, a magical place made of mist, stardust, and Linux servers. This allows you to restore your PC from anywhere in the world, because your backup is in a different dimension to you rather than on a hard drive sitting in your cabinet for *miscellaneous* things.

Anyway, I was able to recover the rest of my files from this, so I guess it served a pretty good *backup for my backup*. Overall, while I'd much rather have a physical backup that's much more convenient if I want to restore my entire Mac (where I don't have to pay 20 dollars and wait a week for a hard drive with the stuff on it to arrive), cloud backups can still be useful for getting specific files.

### Windows Restore Points
If you use Windows instead of MacOS you have the option of using Windows Restore Points, which is like Time Machine except fifty times worse. This has never worked for me, I hate Windows.

### Conclusion
Use Time Machine, consider paying money to back up to the cloud, burn down your Windows install.
