from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    @NOTE: Is the derived from the `django.contrib.auth.models.AbstractUser`
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('user email'),
                              blank=False,
                              unique=True,
                              db_index=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_("Last login time"),
                                      null=True,
                                      blank=True,
                                      editable=False,
                                      help_text="Stores the last login time and date of the user")

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserProfile(models.Model):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    profile_dp = models.ImageField(_('profile picture'), blank=True)
    bio = models.TextField(_('bio'), max_length=255, blank=True)

    company_name = models.CharField(_("Company Name"),
                                    max_length=255,
                                    blank=True,
                                    null=True,
                                    help_text="Collects Company name for which user might be working")
    date_of_birth = models.DateField(_("Date of Birth"),
                                     blank=True,
                                     null=True,
                                     help_text="Field describes the date of birth which will "
                                               "help us find the age of the user")
    last_updated = models.DateTimeField(_("Info updated on"),
                                        null=True,
                                        blank=True,
                                        help_text="This field reflects the date and time"
                                                  " when the user information was last updated")

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
