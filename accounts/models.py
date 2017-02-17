from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.conf import settings

class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
       Creates and saves a User with the given username, email and password.
       """
        now = timezone.now()
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    # now that we've abstracted this class we can add any
    # number of custom attribute to our user class

    # in later units we'll be adding things like payment details!

    objects = AccountUserManager()


class StripeDetail(models.Model):

    class Meta:
        app_label="accounts"

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    stripe_id = models.CharField(max_length=40, default='')
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "%s | for %s " % (self.user_id, self.stripe_id)