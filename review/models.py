from django.db import models

from user.models import Profile


class Review(models.Model):
    givenToUser=models.ForeignKey(Profile, on_delete=models.CASCADE)
    writtenByUser=models.ForeignKey(Profile, on_delete=models.CASCADE)
    reviewText=models.TextField(max_length=1500)

    def __str__(self):
        return self.title
