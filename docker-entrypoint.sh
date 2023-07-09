#!/bin/bash

export DJANGO_SETTINGS_MODULE=spaeti._django.settings


collect-static() {
    rm -rf $SPAETI_STATIC_DIR
    mkdir -p $SPAETI_STATIC_DIR

    lona collect-static $SPAETI_STATIC_DIR \
        --project-root=/app/spaeti \
        -s settings.py

    django-admin collectstatic
}


run-server() {
    exec lona run-server \
        --project-root=/app/spaeti \
        -s settings.py \
        --host=0.0.0.0 \
        --port=8080 \
        --log-level=info \
        --shell-server-url=0.0.0.0:$SPAETI_DEBUG_PORT \
        $@
}


if [ "$1" == "run-server" ] || [ "$1" == "" ]; then
    collect-static
    run-server
else
    exec django-admin $@
fi
