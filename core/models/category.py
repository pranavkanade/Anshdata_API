from django.db import models

from .tag import Tag


class Category(models.Model):
    title = models.CharField(verbose_name='category name', max_length=255, blank=False, null=False)
    wiki = models.URLField(verbose_name='wiki_link', blank=True, null=True)
    tags = models.ManyToManyField(Tag,
                                  verbose_name="related tags",
                                  related_name="categories",
                                  blank=True)
