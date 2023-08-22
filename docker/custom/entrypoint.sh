#!/bin/bash

set -e

if ! [ -z "$GIT_REPO_URL" ] && [ -z "$GIT_BRANCH" ];
then
    echo "Critical failure: GIT_REPO_URL or GIT_BRANCH environment variable not supplied"
    exit 1
fi

if [ "$GIT_REPO_URL" == "$(git config --get remote.origin.url)" ];
then

    git fetch --all
    git switch --discard-changes $GIT_BRANCH


elif [ -d /usr/app/dbt/.git ];
then

    rm -r /usr/app/dbt/*
    git clone --single-branch -b $GIT_BRANCH $GIT_REPO_URL /usr/app/dbt

else

    git clone --single-branch -b $GIT_BRANCH $GIT_REPO_URL /usr/app/dbt

fi

dbt deps
exec dbt "$@"
