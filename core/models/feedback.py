from django.db import models
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    email = models.EmailField(
        _('email'),
        blank=False
    )
    feedback = models.TextField(_("feedback"),
                                blank=True,
                                null=True,
                                default="Test")
