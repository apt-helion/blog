#!/bin/sh

for i in *.png ; do
    convert "$i" -quality 50 "$(basename "${i/.png}")".webp
    sleep 1
done
