from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    street_address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    categories = models.ManyToManyField('projects.ProjectCategory', related_name='competance_categories')

    display_full_name = models.BooleanField(default=True)
    display_email = models.BooleanField(default=True)
    display_phone = models.BooleanField(default=True)
    display_company = models.BooleanField(default=True)
    display_country = models.BooleanField(default=True)
    display_street = models.BooleanField(default=True)
    display_postal = models.BooleanField(default=True)
    display_city = models.BooleanField(default=True)
    display_state = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Review(models.Model):
    #Each review is written by a user
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    author = models.CharField(max_length=50, default=None)
    title = models.CharField(max_length=100, default=None)
    body = models.TextField(max_length=1500, default=None)
    date = models.DateTimeField(timezone.now())
    project = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.title
