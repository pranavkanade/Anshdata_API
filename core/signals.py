from django.db.models import signals
from django.dispatch import dispatcher


def count_students(sender, instance, signal, *args, **kwards):
    from core.models import Course
    for crs in Course.objects.all():
        crs.count_students()
