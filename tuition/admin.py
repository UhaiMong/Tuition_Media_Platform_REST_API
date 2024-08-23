from django.contrib import admin
from .import models
# Register your models here.

admin.site.register(models.Tuition)
admin.site.register(models.Application)
admin.site.register(models.TuitionReview)
admin.site.register(models.AvailableTime)