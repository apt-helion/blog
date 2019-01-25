---
title: Auto Deploying WIth Travis CI And SSH
category: development
date: 2018-11-18
thumbnail: travis-thumb.png
tags: travisci,blogpost
description:
---

For the past few days I've been working on getting auto deployment with Travis CI for this website. If you didn't know already, I write these articles on a localhost server and export a SQL dump to the production server. Now all I would need to do is push the dump in the Git commit and it should import it automatically (as long as all the tests succeed). Anyway, here's how to set it up.

This is the process we will have to go through:

* Set up SSH keys.
* Add the server's copy of the repository as a Git remote.
* Push to the remote.
* SSH into the server and import the SQL dump.

### A Quick Note On Security And Sensitive Information

Connecting from a Travis build box (or any CI system really) to a remote host implies to have the private SSH key on the CI box (_rsa files) and its associated public SSH key on the remote host end (_rsa.pub files). We need to make sure our private key is never seen in the Git repo or in the build logs. Thankfully, the Travis CLI client supports file encryption, so make sure to [install it](https://github.com/travis-ci/travis.rb#installation) so we can encrypt it before pushing it to the repo.

Git also recommends using a separate git user for remote interactions. However, your repositories might be under a separate user (apps, for example), so you'll need to add both those users to a group (deploy, for example). [Here's a guide on how to do that.](https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server)

### SSH keypair

Generate a dedicated SSH key (it is easier to isolate and to revoke).

    ssh-keygen -t rsa -b 4096 -C 'build@travis-ci.org' -f ./deploy\_rsa

Press the `[Enter]` key to use the defaults for the filename and leave the password blank.

Having a RSA key without a password is "OK" for use as a key exclusively used for deployment on Travis-CI because the key will be encrypted using Travis' public key meaning that only Travis can decrypt it. Given that we are "trusting" Travis-CI with the private key there is not much point adding password to it, because the password can easily be "stripped" once the key is decrypted. and, given that Travis needs to "know" the password in order to use the key. If an "attacker" was to gain access to Travis' system and had their private key, the Internet would "break"! seriously, enough NPM packages are automatically published by Travis-CI that it would be "left-pad gate" times a million if Travis were compromised!

Now encrypt the private key to make it readable only by Travis CI (so as we can commit safely too!).

    travis encrypt-file deploy_rsa --add

Copy the public key onto the remote SSH host.

    ssh-copy-id -i deploy_rsa.pub <ssh-user>@<deploy-host>

If you have both git and apps users, make sure to do it for both of them.

Remove the un-encrypted private key file (the public key is mostly okay to push).

    rm -f deploy_rsa

Stage the modified files into Git.

    git add deploy_rsa.enc deploy_rsa.pub

### Remote Git Repository

Assuming you already have your Git repository cloned onto the remote server, the next step is to configure it to allow pushes. Run this to allow Git to accept pushes to a remote with a clean working tree.

    git config --local receive.denyCurrentBranch updateInstead

If you're using CentOS 7, you may also need to update Git to >2.14 as previous versions do not support `receive.denyCurrentBranch updateInstead`.

Once you've done that, make sure that the user and the group can access and modify the repository folder's contents.

    chown apps:deploy -R <repo> chmod g+rw -R <repo>

### Configuring Travis

This part can change by quite a bit depending on what you want to do, so I'll just show you what I did. In our .travis.yml we will add these lines.

```
deploy:
    provider:
    script skip_cleanup: true
    script: deploy/deploy.sh
    on:
        branch: master
```

This will run the script deploy/deploy.sh which looks like this.

```bash
#!/bin/bash
git config --global push.default matching
git remote add deploy ssh://git@$IP:$PORT$DEPLOY_DIR
git push deploy master

ssh apps@$IP -p $PORT <<EOF
    cd $DEPLOY_DIR
    mysql -u $DB_USER -p$DB_PASS blog < migrations/articles.sql
EOF
```

Once you're done with the deploy script, push it to your repository and enable Travis integration for it. The next step is to add environment variables to Travis to keep your IP, SSH port, and deploy directory secret. In the Travis menu, select your repository, click "More options", and click "Settings". Scroll down until you see the list of environment variables. There should be some already there that were added by the Travis CLI in the form encrypted_[hex string]_iv/key. Leave those alone. Add `IP`, `PORT`, and `DEPLOY_DIR` as well as `DB_USER` and `DB_PASS` (if you need them) as variables with their corresponding values. For full security, do not display these values in the build log. Once you've finished that, you're done!


