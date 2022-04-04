from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Account Model


class AccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **other_fields):
        """
        Creates and saves a User with the given infos
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not first_name:
            raise ValueError("Users must have a first name")

        if not email:
            raise ValueError("Users must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **other_fields
    ):
        """
        Creates and saves a SuperUser with the given infos
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.status = "approved"
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    STATUS = [
        ("unapproved", "Unapproved"),
        ("approved", "Approved"),
        ("banned", "Banned"),
    ]

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    status = models.CharField(max_length=15, choices=STATUS, default="unapproved")
    date_registered = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    bio = models.TextField(blank=True, max_length=500)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
