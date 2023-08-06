#!/bin/sh

if [ -x /usr/local/bin/keychain ]; then
  /usr/local/bin/keychain ~/.ssh/id_rsa  
  . ~/.keychain/`/bin/hostname`-sh
fi

DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOST="$(hostname)"
cd $DIR
git push origin master
find . -name "*(*conflict*)*" -print0 | xargs -0 rm
git add . --all
git commit -m 'cron-job on '$HOST
git pull origin master
git push origin master
