#!/bin/bash

if systemctl daemon-reload; then
    echo "daemon reloaded"
else
    echo "problem reloading daemon"
fi

if service gunicorn restart; then
    echo "gunicorn restarted"
else
    echo "Problem restating gunicorn"
fi

if service nginx restart; then
    echo "nginx restarted"
else
    echo "Problem restarting nginx"
fi
