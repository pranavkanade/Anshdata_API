from django.db import models
from .user import User


class Badge(models.Model):
    title = models.CharField(verbose_name='badge name', max_length=255, blank=False, null=False)
    credits_award = models.IntegerField(verbose_name='credits awarded',
                                        blank=True,
                                        null=False,
                                        default=5)
    description = models.TextField(verbose_name="badge description",
                                   blank=True,
                                   null=True)


class Achievement(models.Model):
    title = models.CharField(verbose_name='Achievement name', max_length=255, blank=False, null=False)
    credits_award = models.IntegerField(verbose_name='credits awarded',
                                        blank=True,
                                        null=False,
                                        default=5)
    description = models.TextField(verbose_name="award description",
                                   blank=True,
                                   null=True)
    Signatories = models.ManyToManyField(User,
                                         related_name='signed_on',
                                         blank=True)
