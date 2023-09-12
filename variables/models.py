from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Variables(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variables = models.TextField()


class Permissions(models.Model):
    variables = models.ForeignKey(Variables, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
