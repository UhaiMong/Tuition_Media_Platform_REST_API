from django.db import models
from django.contrib.auth.models import User
from user.models import Profile

# Create your models here.

class AvailableTime(models.Model):
    time = models.CharField(max_length=100)
    
    def __str__(self):
        return self.time
    
class Tuition(models.Model):
    name = models.CharField(max_length=30)
    qualification = models.CharField(max_length=20)
    class_level = models.CharField(max_length=20)
    available_time = models.ManyToManyField(AvailableTime)
    description = models.TextField()
    
    def __str__(self):
        return self.name

CHOICE_STATUS = [
    ('Applied','Applied'),
    ('Accepted','Accepted'),
    ('Rejected','Rejected'),
]
class Application(models.Model):
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    time = models.ForeignKey(AvailableTime,on_delete=models.CASCADE)
    application_status = models.CharField(max_length=20,choices=CHOICE_STATUS,default='Applied')
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name}"
    
CHOICE_RATTING = [
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]
  
class TuitionReview(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    tuition = models.ForeignKey(Tuition,on_delete=models.CASCADE)
    ratting = models.CharField(max_length=10,choices=CHOICE_RATTING)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name}"