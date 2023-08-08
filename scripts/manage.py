#!/bin/bash

export DJANGO_SETTINGS_MODULE=spaeti._django.settings

exec django-admin $@
