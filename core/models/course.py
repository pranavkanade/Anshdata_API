from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .user import User
from .tag import Tag
from .category import Category

from .achievement import Achievement


class Course(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    subject = models.CharField(_("Title"),
                               max_length=255,
                               blank=True,
                               null=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="courses",
                               help_text="Refers to the creator account of the course")
    # TODO: we hold this back
    tagged_to = models.ManyToManyField(Tag,
                                       verbose_name="related tags",
                                       related_name='courses',
                                       blank=True)
    # TODO: we hold this back
    # One course can only belong to single category at first
    category = models.ForeignKey(Category,
                                 verbose_name="related category",
                                 related_name='courses',
                                 blank=False,
                                 on_delete=models.PROTECT)
    # TODO: Add this aspect of the course in the api which is use to list for enrollment
    is_published = models.BooleanField(verbose_name="is published",
                                       default=False,
                                       blank=True)
    rating = models.FloatField(verbose_name='overall rating',
                               default=0,
                               blank=True)
    is_accepting_contrib = models.BooleanField(verbose_name="is accepting contribution",
                                               default=False,
                                               blank=True)
    credit_points = models.IntegerField(verbose_name='credits points to be gained',
                                        blank=True,
                                        null=False,
                                        default=0)
    students_count = models.IntegerField(verbose_name='total enrollment',
                                         blank=True,
                                         null=False,
                                         default=0)
    description = models.TextField(_("Course's Description"),
                                   blank=True,
                                   null=True,
                                   default="New Course")
    # TODO: Hold this back
    intro = models.URLField(verbose_name='Intro video')
    # TODO: Estimated time needs to be calculated
    # estimate_time_required = models.IntegerField(_("Estimate Time"),
    #                                              default=0,
    #                                              blank=True,
    #                                              null=False,
    #                                              help_text="Approx. time required to complete the course")
    reviewers = models.ManyToManyField(User,
                                       blank=True,
                                       related_name="courses_reviewed")
    is_approved = models.BooleanField(verbose_name="is approved to publish",
                                      default=False,
                                      blank=True)
    reviewer_rating = models.FloatField(verbose_name='overall rating',
                                        default=0,
                                        blank=True)
    achievement = models.OneToOneField(Achievement,
                                       verbose_name="course completion award",
                                       blank=True,
                                       null=True,
                                       on_delete=models.PROTECT,
                                       related_name="course")


class Module(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    description = models.TextField(_("Module's Description"),
                                   blank=True,
                                   null=True,
                                   default="New Module")
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="modules",
                               help_text="Refers to the course this unit belongs to")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="modules",
                               help_text="Refers to the creator account of the modules")
    reference = models.TextField(_("Reference Material"),
                                 blank=True,
                                 null=True,
                                 max_length=1000)


class Lesson(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    description = models.TextField(_("Lesson's Description"),
                                   blank=True,
                                   null=True,
                                   default="New Lesson")
    lecture = models.URLField(_("Video URL"),
                              blank=True,
                              null=True)
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               editable=True,
                               related_name="lessons")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="lessons",
                               help_text="Refers to the creator account of the lessons")


class Assignment(models.Model):
    title = models.CharField(_("Title"),
                             max_length=255,
                             blank=False,
                             null=False)
    instruction = models.TextField(_("assignment instruction"),
                                   blank=True,
                                   null=True,
                                   default="Test Course")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="assignments_contributed",
                               help_text="Refers to the creator account of the course")

    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               editable=True,
                               related_name="assignments")
    module = models.ForeignKey(Module,
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

    credit_points = models.IntegerField(verbose_name='credits points to be gained',
                                        blank=True,
                                        null=False,
                                        default=0)
    reference = models.TextField(_("Reference Material"),
                                 blank=True,
                                 null=True,
                                 max_length=1000)

    # estimate_time_required = models.IntegerField(_("Estimate Time"),
    #                                              default=0,
    #                                              blank=True,
    #                                              null=False,
    #                                              help_text="Approx. time required to complete the assignment in hrs")


class CourseProgress(models.Model):
    candidate = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False,
                                  related_name="enrollments",
                                  help_text="Refers to the candidate who is taking on the associated course")
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False,
                               related_name="enrollments",
                               help_text="Refers to the course that the candidate has enrolled in")
    date_enrolled = models.DateTimeField(_('date enrolled'),
                                         default=timezone.now)
    date_completed = models.DateTimeField(_('date completed'),
                                          blank=True,
                                          null=True)
    # TODO: Add last visited
    current_lesson = models.OneToOneField(Lesson,
                                          on_delete=models.PROTECT,
                                          blank=True,
                                          null=True,
                                          help_text="Refers to the last lesson the user had subscribe to")
    current_assignment = models.OneToOneField(Assignment,
                                              on_delete=models.PROTECT,
                                              blank=True,
                                              null=True,
                                              help_text="Refers to the last assignment the user had subscribe to")
    credit_earned = models.IntegerField(_('credit earned'),
                                        blank=True,
                                        default=0,
                                        help_text="Credit points a user has earned till now in the course")

    class Meta:
        unique_together = (("candidate", "course"), )


class LessonCompleted(models.Model):
    enrollment = models.ForeignKey(
        CourseProgress,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="completed_lessons",
        help_text="link to which user and course we this record belongs to"
    )
    module = models.IntegerField(
        _('module id'),
        blank=True,
        default=0,
        help_text=("This field holds the record of which "
                   "module's lesson user has  completed")
    )

    lesson = models.IntegerField(
        _('lesson id'),
        blank=True,
        default=0,
        help_text=("This field holds the record of which "
                   "lesson user has  completed")
    )


class AssignmentCompleted(models.Model):
    enrollment = models.ForeignKey(
        CourseProgress,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="completed_assignments",
        help_text="link to which user and course we this record belongs to"
    )

    module = models.IntegerField(
        _('module id'),
        blank=True,
        default=0,
        help_text=("This field holds the record of which "
                   "module's asignment user has completed")
    )

    lesson = models.IntegerField(
        _('lesson id'),
        blank=True,
        default=0,
        help_text=("This field holds the record of which "
                   "lesson's assignment user has completed")
    )

    assignment = models.IntegerField(
        _('assignment id'),
        blank=True,
        default=0,
        help_text=("This field holds the record of which "
                   "assignment user has completed")
    )
