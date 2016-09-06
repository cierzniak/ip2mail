#!/usr/bin/env bash

if [[ $# == 0 ]] ; then
    APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    cd ${APP_DIR}
    sleep 120
    ./apps/Main.py
fi