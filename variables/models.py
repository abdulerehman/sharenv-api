from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Variables(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variables = models.TextField()
    password = models.CharField(max_length=100, null=True, blank=True)