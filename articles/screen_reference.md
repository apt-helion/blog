---
title: A Reference Of Linux Screen Commands Because I Keep Forgetting Them
category: miscellaneous
date: 2019-06-12
thumbnail: default-thumb.png
tags: linux,screen
description:
---

In Linux `screen` is a command that allows you to:

* Use multiple shell windows from a single SSH session.
* Keep a shell active even through network disruptions.
* Disconnect and re-connect to a shell sessions from multiple locations.
* Run a long running process without maintaining an active shell session.

### Starting Linux Screen

Screen is started from the command line just like any other command:

```
[root@okcomputer ~]# screen
```

You are now inside of a window within screen. This functions just like a
normal shell except for a few special characters.

Screen uses the command `Ctrl-a”` as a signal to send commands to screen
instead of the shell.

For example, `Ctrl-a ?` gives you the key bindings page.

### Detaching From Screen

You can detach from the window using `Ctrl-a d`.

### Reattach to Screen

If your connection drops or you have detached from a screen, you can re-attach
by just running:

```
[root@okcomputer ~]# screen -r
```

### Stopping Screen

To stop the screen session, enter `exit` into the shell or use `Ctrl-a k`.

### Other Commands

To run a single command in screen and detach:

```
[root@okcomputer ~]# screen -dm ./myscript.sh
```

To run multiple commands:

```
[root@okcomputer ~]# screen -dm bash -c "sleep 10; myscript.sh"
```

To list all sessions:

```
[root@okcomputer ~]# screen -list
```

Please note that when a program terminates, screen (per default) kills the
window that contained it.
