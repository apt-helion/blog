---
title: Writing A Simple Ruby Script To Automate Nmap
category: development
date: 2018-10-29
thumbnail: ruby-nmap-thumb.png
tags: ruby,nmap
description:
---

An nmap scan should always be the first thing to do when you start a box, and since I'm too lazy to write `nmap -sV -sC -oA initial box_ip` (and I want a progress bar instead of having to constantly press a button to see progress), we're just going to write a script to do it for us.

I'm using Ruby for this because I think it's just as readable as Python (so I don't have to explain as much) and because I'm not bothered to learn how to do this in Python, which means that this is the first time I've ever shown code on this website that isn't Python.

Anyway, to do this we will use [a class from Ruby's standard library called PTY](https://ruby-doc.org/stdlib-2.4.1/libdoc/pty/rdoc/PTY.html). `PTY` allows you to spawn an external process and then interact with that process by using puts to write to it's `stdin` and gets to read from it's `stdout`.

```ruby
#!/usr/bin/ruby

require 'pty'
cmd = "nmap -sV #{ARGV[0]}"

PTY.spawn( cmd ) do |stdout, stdin, pid|
  loop do
    stdin.puts ' '
    puts stdout.gets.chomp
    sleep 0.1
  end
end
```

This is our initial code. It runs nmap with the box IP as an argument and every 0.1 seconds, it sends a space character to stdin and prints stdout so we can see the progress of the scan. This works but right now we are only running nmap with -sV, so now we should add all the arguments we need.

```ruby
#!/usr/bin/ruby

require 'pty'
require 'fileutils'

FileUtils.mkdir_p 'nmap'
cmd = "nmap -sV -sC -oA nmap/initial #{ARGV[0]}"

PTY.spawn( cmd ) do |stdout, stdin, pid|
  loop do
    stdin.puts ' '
    puts stdout.gets.chomp

    running = %x[ ps -p #{pid} -o comm= ]
    if running.include? "defunct"
      break
    end

    sleep 0.1
  end
end
```

Now we are creating a folder where all the nmap scripts will be stored using the library 'fileutils' and we've edited the 'cmd' variable to use all the arguments. I've also added a check to see if nmap has finshed in order to break out of the loop by checking if the process name includes the words 'defunct'.

If you run this you will see that stdout becomes very messy as the progress is constantly being called. Let's get that progress bar working.

```ruby
#!/usr/bin/ruby

require 'pty'
require 'fileutils'
require 'progress_bar'

FileUtils.mkdir_p 'nmap'
cmd = "nmap -sV -sC -oA nmap/initial #{ARGV[0]}"

$syn_bar = ProgressBar.new
$srv_bar = ProgressBar.new
$nse_bar = ProgressBar.new

$syn_progress = 0
$srv_progress = 0
$nse_progress = 0

$step = "init"

def increment_bar(stdout)
  new_status = stdout.match(/[[:digit:]]{1,2}\.[[:digit:]]{2}/)
  new_status ? new_status = new_status[0].to_i : return

  if stdout.include? "SYN Stealth Scan"
    if $step != "syn"
      puts "Step 1/3 [SYN Stealth Scan]"
      $step = "syn"
    end

    inc_amount = new_status - $syn_progress
    $syn_progress = new_status
    $syn_bar.increment! inc_amount
  elsif stdout.include? "Service"
    if $step != "srv"
      puts "Step 2/3 [Service Scan]"
      $step = "srv"
    end

    inc_amount = new_status - $srv_progress
    $srv_progress = new_status
    $srv_bar.increment! inc_amount
  elsif stdout.include? "NSE Timing"
    if $step != "nse" && $step != 'init'
      # NSE Timing shows up before it actually begins
      puts "Step 3/3 [NSE]"
      $step = "nse"
    end

    inc_amount = new_status - $nse_progress
    $nse_progress = new_status
    $nse_bar.increment! inc_amount
  end
end

PTY.spawn( cmd ) do |stdout, stdin, pid|
  loop do
    stdin.puts ' '
    response = stdout.gets.chomp

    increment_bar(response)

    running = %x[ ps -p #{pid} -o comm= ]
    if running.include? "defunct"
      break
    end

    sleep 0.1
  end
end
```

This is a really quick and dirty way of getting a progress bar using the library `progress_bar`. Make sure to install it with:

    gem install progress_bar

Obviously I'm not super proud this script, it's actually pretty terrible for my standards, so much so that I don't want to explain it. But it does what I wanted it to and only took me 5 minutes to write. Someday I may comeback to it to clean up all the repeating code and stop using so many global variables (but I say that about all the code I write, so whatever).

Now I can move save this as `/opt/scan-box` and call it with `/opt/scan-box box_ip`. You could also put it in `/bin` so you can call it with just `scan-box box_ip`, but I don't like doing that.
