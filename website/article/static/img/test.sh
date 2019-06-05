#!/bin/sh

for i in *.jpg ; do
    convert "$i" -quality 50 "$(basename "${i/.jpg}")".webp
    sleep 5
done
