#!/bin/sh
flask db upgrade
exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 start:app