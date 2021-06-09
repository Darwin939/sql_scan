from django.db import models

# Create your models here.
class Website(models.Model):
    url = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.BooleanField(default=False)
    
class Vulnerability(models.Model):
    url =  models.CharField(max_length=500)
    type =  models.CharField(max_length=500)
    site =  models.ForeignKey(Website, on_delete=models.CASCADE)