from django.db import models
from user.models import Profile
from util.models import SingletonModel
from django.core.exceptions import ValidationError

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from datetime import timedelta
from django.utils import timezone

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class ProjectCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    participants = models.ManyToManyField(Profile, related_name='project_participants')
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='project_category')
    requested_promotion = models.BooleanField(default=False)

    OPEN = 'o'
    INPROG = 'i'
    FINISHED = 'f'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (INPROG, 'In progress'),
        (FINISHED, 'Finished'),
    )
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=OPEN)


    def __str__(self):
        return self.title

class PromotionSettings(SingletonModel):
    pool_size = models.IntegerField(default=20)
    display_amount = models.IntegerField(default=1)
    promotion_fee = models.IntegerField(default=0.0)
    duration_in_days = models.IntegerField(default=7)

    def __str__(self):
        return "Promotion Setting"

    def clean(self):
        validation_errors = []
        if self.pool_size < self.display_amount:
            validation_errors.append(ValidationError("Pool size cannot be smaller than Display amount"))
        if self.is_negative(self.pool_size):
            validation_errors.append(ValidationError("Pool size cannot be negative."))
        if self.is_negative(self.display_amount):
            validation_errors.append(ValidationError("Display amount cannot be negative."))
        if self.is_negative(self.promotion_fee):
            validation_errors.append(ValidationError("Promotion fee cannot be negative."))
        if self.duration_in_days < 1:
            validation_errors.append(ValidationError("Duration in days must have a valid duration length."))

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)

    def is_negative(self, number):
        return number < 0

class PromotedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="promoted_project")
    start = models.DateTimeField(default=timezone.now, blank=True)
    def get_default_end_date():
        promotion_settings = PromotionSettings.load()
        return timezone.now() + timedelta(days=promotion_settings.duration_in_days)
    end = models.DateTimeField(default=get_default_end_date, blank=True)

            
    def __str__(self):
        return self.project.title

    def clean(self):
        for active_promotion in ActivePromotion.objects.all():
            if active_promotion.promoted_project.project == self.project:
                raise ValidationError("The project is already in an active promotion!")

class ActivePromotion(models.Model):
    promoted_project = models.ForeignKey(PromotedProject, on_delete=models.CASCADE, related_name="active_promotion")
    
    def category(self):
        return self.promoted_project.project.category

    def count_promotions_in_category(self, category):
        return ActivePromotion.objects.all().filter(promoted_project__project__category=category).count()

    def clean(self):
        settings = PromotionSettings.load()
        if self.count_promotions_in_category(self.category()) >= settings.pool_size:
            raise ValidationError("The promotion pool for this category is full!")
        if self.promoted_project.end < timezone.now():
            raise ValidationError("The promotion has already expired")
        try:
            ActivePromotion.objects.get(promoted_project=self.promoted_project)
            is_promoted = True
        except:
            is_promoted = False    
        if is_promoted:
            raise ValidationError("The project is already promoted!")

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    budget = models.IntegerField(default=0)


    AWAITING_DELIVERY = 'ad'
    PENDING_ACCEPTANCE = 'pa'
    PENDING_PAYMENT = 'pp'
    PAYMENT_SENT = 'ps'
    DECLINED_DELIVERY = 'dd'
    STATUS_CHOICES = (
        (AWAITING_DELIVERY, 'Waiting for delivery'),
        (PENDING_ACCEPTANCE, 'Delivered and waiting for acceptance'),
        (PENDING_PAYMENT, 'Delivery has been accepted, awaiting payment'),
        (PAYMENT_SENT, 'Payment for delivery is done'),
        (DECLINED_DELIVERY, 'Declined delivery, please revise'),
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=AWAITING_DELIVERY)
    feedback = models.TextField(max_length=500, default="")

    read = models.ManyToManyField(Profile, related_name='task_participants_read')
    write = models.ManyToManyField(Profile, related_name='task_participants_write')
    modify = models.ManyToManyField(Profile, related_name='task_participants_modify')


    def __str__(self):
        return  str(self.id) + " " + self.title

    def accepted_task_offer(task):
        task_offer = None
        try:
            task_offer = task.taskoffer_set.get(status='a')
        except TaskOffer.DoesNotExist:
            pass
        return task_offer


class Team(models.Model):
    name = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="teams")
    members = models.ManyToManyField(Profile, related_name='teams')
    write = models.BooleanField(default=False)


    def __str__(self):
        return  self.task.project.title + " - " + self.task.title + " - " + self.name

def directory_path(instance, filename):
    return 'static/uploads/tasks/{0}/{1}'.format(instance.task.id, filename)


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=directory_path, storage=OverwriteStorage())

    def name(self):
        parts = self.file.path.split("/")
        file_name = parts[len(parts) - 1]
        return file_name

class TaskFileTeam(models.Model):
    file = models.ForeignKey(TaskFile, on_delete=models.CASCADE, related_name="teams")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="file")
    name = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    modify = models.BooleanField(default=False)

class Delivery(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="delivery")
    file = models.FileField(upload_to=directory_path)
    comment = models.TextField(max_length=500)
    delivery_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="deliveries")
    delivery_time = models.DateTimeField(auto_now=True)
    responding_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="responded_deliveries", blank=True, null=True)
    responding_time = models.DateTimeField(blank=True, null=True)

    ACCEPTED = 'a'
    PENDING = 'p'
    DECLINED = 'd'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (PENDING, 'Pending'),
        (DECLINED, 'Declined'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING)
    feedback = models.TextField(max_length=500)


class TaskOffer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    offerer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=500)

    ACCEPTED = 'a'
    PENDING = 'p'
    DECLINED = 'd'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (PENDING, 'Pending'),
        (DECLINED, 'Declined'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING)
    feedback = models.TextField(max_length=500)
