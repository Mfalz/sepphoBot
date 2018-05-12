#!/usr/bin/env bash

git fetch origin master

local_commit=$(git rev-list --branches --max-count=1)
remote_commit=$(git rev-list --remotes --max-count=1)

if [[ ${local_commit} != ${remote_commit} ]] ; then
    echo "remote has some new commits"
    git pull
else
    echo "up to date with remote"
fi