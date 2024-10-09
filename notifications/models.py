from django.db import models

class Notification(models.Model):
    TYPE_CHOICES = [
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('image', 'Image'),
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    content =models.CharField(max_length=100000,blank=True,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.created_at}"
