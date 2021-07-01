from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig

class UsersConfig(AppConfig):
    name = "rattletest.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import rattletest.users.signals  # noqa F401
        except ImportError:
            pass


class ModifiedAccountConfig(AccountConfig):
    default_auto_field = 'django.db.models.AutoField'

class ModifiedSocialAccountConfig(SocialAccountConfig):
    default_auto_field = 'django.db.models.AutoField'