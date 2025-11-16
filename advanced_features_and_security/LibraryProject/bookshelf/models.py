from django.db import models

# Create your models here.
from django.conf import settings

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
