## Notes

Sometimes I have tiny little personal web apps I want to write but the overhead of starting a new project gets in the way. This [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) template is designed to help me get over that.

- Django, Tailwind, HTMX
- Deployed to Fly
- Behind Tailscale, piggybacking on Tailscale auth

Since this is pretty specific to _me_ and the way _I_ want to write things, I'm unlikely to accept PRs. Feel free to ask first by opening and issue or emailing me or something! I don't want you to waste your time with a PR that I won't accept.

Excception: if there's something on my [TODO](#todo) list below, heck yeah I'll take a PR for it!

### Deployment

Generate a [tailscale auth key](https://login.tailscale.com/admin/settings/keys) - ephemeral, reusable.

```
fly launch [--org jacobian-org]
fly secrets set TAILNET_DOMAIN=clever-sushi.ts.net
fly secrets set TAILSCALE_AUTHKEY=....
fly deploy
```

### Admin access / permissions

Users are auto-created from Tailscale auth, but are created without perms. To add permissions:

```
fly console
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username="jacob").update(is_staff=True, is_superuser=True)
```

### Making an app public

See `fly.toml` - there are lines commented out at the bottom that make things public. Think about whether to remove `TailscaleAuthMiddleware` or nah.

## TODO:

- [ ] figure out testing:
  - want to use https://github.com/hackebrot/pytest-cookies, but installing it fails with an error installing pyyaml, see e.g. https://github.com/python-poetry/poetry/issues/8287, which I can't figure out a workout for, so punting on testing for now
- [ ] automate admin upgrade
- [ ] try to fix the `node-1`, `node-2`, etc. thing
  - Fly doesn't clean up old apps before deploying new ones (and doesn't have a deployment startegy that does), so when the new app bootstraps Tailscale sees it as a duplicate and gives it a unique name. Is there a fix/workaround?
- [ ] stream db to litestream as backup/sync
- [ ] automate initial fly launch config - can probably prompt for authkey, domain, and execute from the post-gen hook