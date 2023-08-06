#!/bin/sh

if [ -x /usr/local/bin/keychain ]; then
  /usr/local/bin/keychain ~/.ssh/id_rsa  
  . ~/.keychain/`/bin/hostname`-sh
fi

DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOST="$(hostname)"
cd $DIR
find . -name "*(*conflict*)*" -print0 | xargs -0 rm
git push
git reset HEAD
git checkout -- .
git push
git pull origin master
