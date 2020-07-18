from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save

from baseapp.management.predictadoptionspeed import predict_speed


# Django User Management -- ignore
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Django User Creation -- ignore
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this site.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


# Breed model - create database and model/object
class Breed(models.Model):
    name = models.CharField(max_length=100)
    csv_id = models.IntegerField(default=0)
    adaptability = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    energy = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    friendliness = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    health_grooming = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    trainability = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    size = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.name


# Dog model - create database and model/object
class Dog(models.Model):
    pet_id = models.CharField(max_length=100, default=0)
    name = models.CharField(max_length=500)
    age = models.IntegerField(default=0)
    breed_one = models.ForeignKey(Breed, on_delete=models.CASCADE, null=False)
    breed_two = models.ForeignKey(Breed, on_delete=models.CASCADE, null=True, related_name='breed_two', default=None, blank=True)
    gender = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    maturity_size = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(4)])
    vaccinated = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(3)])
    dewormed = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(3)])
    sterilized = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(3)])
    health = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(3)])
    # Calculate adoption speed when model created
    adoption_speed = models.PositiveIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)],
                                                 editable=False)

    def __str__(self):
        return self.name


# Calculate adoption speed when model edited
@receiver(pre_save, sender=Dog)
def get_adoption_speed(sender, instance, *args, **kwargs):
    age = instance.age
    gender = instance.gender
    breed_two = instance.breed_two
    maturity_size = instance.maturity_size
    dewormed = instance.dewormed
    health = instance.health
    has_breed2 = 0
    if breed_two is not None:
        has_breed2 = 1

    instance.adoption_speed = predict_speed(age, has_breed2, gender, maturity_size, dewormed, health)
    return
