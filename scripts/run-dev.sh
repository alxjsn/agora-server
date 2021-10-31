#!/bin/sh

. venv/bin/activate
parcel watch js-src/index.ts --dist-dir app/static/js &
flask run -h 0.0.0.0 -p 5000