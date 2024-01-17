FROM python:3.12-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code

# Install Tailscale
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://pkgs.tailscale.com/stable/debian/bullseye.noarmor.gpg | tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null && \
    curl -fsSL https://pkgs.tailscale.com/stable/debian/bullseye.tailscale-keyring.list | tee /etc/apt/sources.list.d/tailscale.list && \
    apt-get update && \
    apt-get -y install tailscale

# Buid app
RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY . /code

RUN poetry run python manage.py tailwind build && \
    poetry run python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
