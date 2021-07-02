from django.db import models
from django.utils import timezone
from authentication.models import User

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_last_modified = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.title
