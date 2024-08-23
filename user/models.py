from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    educational_qualification = models.CharField(max_length=100)
    mobileNumber = models.CharField(max_length=12)
    profileImage = models.ImageField(upload_to="user/images")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"