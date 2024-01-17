#!/bin/sh

tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock &
tailscale up --authkey=${TAILSCALE_AUTHKEY} --hostname=${FLY_APP_NAME}
tailscale serve --bg 8000

poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000