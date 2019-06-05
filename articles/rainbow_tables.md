---
title: I Learn To Draw Diagrams and You Learn About Rainbow Tables
category: infosec
date: 2018-07-17
thumbnail: rainbow-thumb.webp
tags: rainbow,drawing
description:
---

As most people should know, a Rainbow Table is a way of mapping a plaintext to it's hash by storing the plaintext -> hash combo in a file on the hard drive. However, storing every hash individually takes up an amount of space nobody could ever have. There is much more going under the hood of a Rainbow Table, and today we are going to look at how it attempts to minimise the memory it takes up.

Generating a Rainbow Table uses two key functions: a hash function and a reduction function. The hash function maps a plaintext to a hash.

![image-alternative](/website/article/static/img/hash.webp)

While the reduction function maps a hash to a plaintext. The reduction function obviously does not generate the original plaintext of the hash, it is not an *inverse* hashing function because that should be impossible. What the reduction function does is create a new plaintext from the hash. The reduction function is a key part of the Rainbow Table and is very complicated. So for the purposes of this article, we will keep it simple. In our case we will have a reduction function that takes the first 7 characters of a hash.

![image-alternative](/website/article/static/img/reduction.webp)

A rainbow table is made of up of chains of hashes and reductions. A chain starts with an arbitrary plaintext and ends with a hash. The plaintext will go through the process of being hashed and reduced millions of times. The table only stores the starting plaintext, and the final hash you choose to end with, and so a chain "containing" millions of hashes can be represented with only a single starting plaintext, and a single finishing hash.

![image-alternative](/website/article/static/img/chain.webp)

Now that we have our table of chains. We can start looking for an unknown plaintext with a hash. Here is the process:

![image-alternative](/website/article/static/img/rainbow-process.webp)

In this way you check through the hashes in the chains, which aren't actually stored anywhere on disk, by iterating column by column through the table of chains, backwards from the last column in the chain, to the starting plaintext.

The reason they're called Rainbow Tables is because each column uses a different reduction function. If each reduction function was a different color, and you have starting plaintexts at the top and final hashes at the bottom, it would look like a rainbow (a very vertically long and thin one).


