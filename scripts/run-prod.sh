#!/bin/sh

. venv/bin/activate
nginx
uwsgi prod.ini