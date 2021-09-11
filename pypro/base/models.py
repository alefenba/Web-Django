from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """Creates and saves a User with the given email and password"""
        if not email:
            raise ValueError(' The given email must be set')
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

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True. ')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True. ')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    App base User class
    Email and password are required. Other fields are optional
     """

    first_name = models.CharField(('first name'), max_length=30, blank=True)
    email = models.CharField(('email address'), max_length=30, unique=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(' Designates wheter the user can log into this admin site'),
    )
    is_active = models.BooleanField(
        ('activate'),
        default=True,
        help_text=(
            'Designates wheter this user should be treated as activate'
            'Unselect this instead of deleting accounts.'
        ),

    )
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between
        """
        full_name = '%s' % (self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user"""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
