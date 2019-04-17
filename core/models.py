from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email address must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """

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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserProfile(models.Model):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
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
                                        editable=False,
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


class Course(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    # description = models.TextField(_("Course's Description"),
    #                                blank=True,
    #                                null=True,
    #                                default="Test Course")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="courses",
                               help_text="Refers to the creator account of the course")
    # estimate_time_required = models.IntegerField(_("Estimate Time"),
    #                                              default=0,
    #                                              blank=True,
    #                                              null=False,
    #                                              help_text="Approx. time required to complete the course")
    students = models.ManyToManyField(User,
                                      blank=True,
                                      related_name="enrolled_in")


class Unit(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    # description = models.TextField(_("Unit's Description"),
    #                                blank=True,
    #                                null=True,
    #                                default="Test Unit")
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="units",
                               help_text="Refers to the course this unit belongs to")


class Lesson(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    # link_to_lecture = models.URLField(_("Video URL"),
    #                                   blank=True,
    #                                   null=True,
    #                                   default="https://www.youtube.com/watch?v=6MSksJhPcVA")
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False,
                             editable=True,
                             related_name="lessons")


class Assignment(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    # description = models.TextField(_("Course's Description"),
    #                                blank=True,
    #                                null=True,
    #                                default="Test Course")

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="assignments_contributed",
                               help_text="Refers to the creator account of the course")

    # Assignments may not be related to any one single lesson or unit.
    # In that case lesson FK will be left blank.
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               editable=True,
                               related_name="assignments")
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             editable=True,
                             related_name="assignments")
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               editable=True,
                               related_name="assignments")

    # estimate_time_required = models.IntegerField(_("Estimate Time"),
    #                                              default=0,
    #                                              blank=True,
    #                                              null=False,
    #                                              help_text="Approx. time required to complete the assignment in hrs")
