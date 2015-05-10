# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy
from faces.api.apps.authorization import facebook_download_image
from faces.lib.django import POSIX_ZERO
from faces.lib.django.models import ModelMixins
from faces.lib.django.querysets import ValidityQuerySet


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        try:
            user = self.get_by_natural_key(username)
        except User.DoesNotExist:
            user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def user_post_save(sender, instance, created, **kwargs):
        """ This method is executed whenever an user object is saved
        """
        if created:
            image = facebook_download_image(instance.facebook_id)
            instance.avatar = image
            instance.save()


    def get_queryset(self):
        return ValidityQuerySet(self.model, using=self._db)


class Gender(object):
    MALE = "male"
    FEMALE = "female"

    CHOICES = (
        (MALE, "male"),
        (FEMALE, "female")
    )


class User(AbstractBaseUser, PermissionsMixin, ModelMixins):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    username = models.CharField(unique=True, max_length=255, verbose_name=ugettext_lazy("username"))
    facebook_id = models.CharField(unique=True, max_length=255, verbose_name=ugettext_lazy("facebook id"))
    avatar = models.ForeignKey("images.ImageModel", related_name="+", null=True, blank=True)

    email = models.EmailField(unique=True, verbose_name=ugettext_lazy("email"))
    name = models.CharField(null=True, default=None, max_length=255, verbose_name=ugettext_lazy("name"))
    facebook_access_token = models.CharField(max_length=255, null=True, blank=True)

    face_api_id = models.CharField(max_length=255, null=True, blank=True)

    # Special fields
    created_at = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=ugettext_lazy('Created at'))
    modified_at = models.DateTimeField(blank=True, auto_now=True,
                                       verbose_name=ugettext_lazy('Modified at'))
    is_staff = models.BooleanField(ugettext_lazy('staff status'), default=False,
                                   help_text=ugettext_lazy('Designates whether the user can log into this admin '
                                                           'site.'))

    deleted_at = models.DateTimeField(blank=False, default=POSIX_ZERO, verbose_name=ugettext_lazy('Deleted at'))

    gender = models.CharField(max_length=255, choices=Gender.CHOICES, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    recommendation = models.ForeignKey("products.ProductModel", null=True, blank=True)
    previous_recommendation = models.ForeignKey("products.ProductModel", null=True, blank=True, related_name="previous_reccomendation")

    def get_short_name(self):
        return self.username

    @property
    def has_gender(self):
        return self.gender is not None

    @property
    def is_male(self):
        return self.gender == Gender.MALE

    def is_female(self):
        return self.gender == Gender.FEMALE
