from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import uuid

# Create your models here.

class Chat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.CharField(max_length=1000)
    slug = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date=models.DateField()

admin.site.register(Chat)