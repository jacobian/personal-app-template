from django.contrib.auth import get_user_model


class TailscaleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        email = request.headers.get("Tailscale-User-Login")
        UserModel = get_user_model()
        try:
            request.user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            request.user = self._create_user(email)

        return self.get_response(request)

    # This all could be a lot more complex if it were something more generic --
    # need to consider perms, admin status, etc. Maybe someday.
    def _create_user(self, email):
        name = email.split("@", 1)[0]
        return get_user_model().objects.create_user(username=name, email=email)
