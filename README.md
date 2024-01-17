## Notes

Sometimes I have tiny little personal web apps I want to write but the overhead of starting a new project gets in the way. This [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) template is designed to help me get over that.

- Django, Tailwind, HTMX
- Deployed to Fly
- Behind Tailscale, piggybacking on Tailscale auth

These end up being private apps -- no public interface, only accessible on my Tailnet. In other words this is sorta a replaecment for running things in a homelab or similar. A personal Intranet, if you will.

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
