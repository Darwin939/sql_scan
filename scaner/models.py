from django.db import models
from django.db.models.base import Model

# Create your models here.
class Website(models.Model):
    url = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.BooleanField(default=False)
    
class Vulnerability(models.Model):
    url =  models.CharField(max_length=500)
    type =  models.CharField(max_length=500)
    site =  models.ForeignKey(Website, on_delete=models.CASCADE)

class Log(models.Model):
    text = models.TextField()
    # site =  models.ForeignKey(Website, on_delete=models.CASCADE)