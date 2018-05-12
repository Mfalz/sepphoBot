#!/usr/bin/env bash

pushd /home/pi/workspace/sepphobot
git fetch origin master

local_commit=$(git rev-list --branches --max-count=1)
remote_commit=$(git rev-list --remotes --max-count=1)

if [[ ${local_commit} != ${remote_commit} ]] ; then
    echo "remote has some new commits"
    git pull
    sudo systemctl restart sepphobot
else
    echo "up to date with remote"
fi

popd