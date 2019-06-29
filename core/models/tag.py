from django.db import models


class Tag(models.Model):
    title = models.CharField(verbose_name='tag name', max_length=255, blank=False, null=False)
    wiki = models.URLField(verbose_name='wiki_link', blank=True, null=True)
