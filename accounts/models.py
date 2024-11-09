from django.db import models
from django.contrib.auth.models import User


class newUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plaintext_password = models.CharField(max_length=255)
    def __str__(self):
        return f"Password for {self.user.username}"
