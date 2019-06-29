from django.db import models
from django.utils.translation import gettext_lazy as _

from .tag import Tag


class Social(models.Model):
    facebook = models.URLField(verbose_name='facebook', blank=True, null=True)
    linked_in = models.URLField(verbose_name='linked in', blank=True, null=True)
    twitter = models.URLField(verbose_name='twitter', blank=True, null=True)
    github = models.URLField(verbose_name='github', blank=True, null=True)
    website = models.URLField(verbose_name='website', blank=True, null=True)
    blog = models.URLField(verbose_name='blog', blank=True, null=True)


class Profile(models.Model):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    profile_dp = models.ImageField(_('profile picture'), blank=True)
    bio = models.TextField(_('bio'), max_length=255, blank=True)

    interests = models.ManyToManyField(Tag,
                                       verbose_name="tags interested in",
                                       related_name='favored_by',
                                       blank=True)
    expertise = models.ManyToManyField(Tag,
                                       verbose_name="tags expert in",
                                       related_name='experts',
                                       blank=True)
    # TODO: Add model to store education
    # Education
    # TODO: Add model to store publication
    # Publications
    credit_points = models.IntegerField(verbose_name='credits remaining',
                                        blank=True,
                                        null=False,
                                        default=25)
    total_credits_spent = models.IntegerField(verbose_name='credits spent in total',
                                              blank=True,
                                              null=False,
                                              default=0)
    # TODO: Add model to store location
    # TODO: Add model to store designation

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
