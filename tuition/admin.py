from django.contrib import admin
from .import models
# for email sending
from rest_framework.parsers import MultiPartParser,FormParser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class TuitionModelAdmin(admin.ModelAdmin):
    list_display = ['name','qualification','class_level','description']
    
admin.site.register(models.Tuition,TuitionModelAdmin)
class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ['application_status','application_date']

    def save_model(self,request,obj,form,change):
        obj.save()
        if obj.application_status == "Accepted":
            email_subject = "Your Application is accepted!"
            email_body = render_to_string('ApplicationStatus.html',{'user':obj.profile.user,'tutor':obj.tuition.name,'date':obj.application_date,'status':obj.application_status})
            email = EmailMultiAlternatives(email_subject,'',to=[obj.profile.user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
        
  
admin.site.register(models.Application,ApplicationModelAdmin)

admin.site.register(models.TuitionReview)
admin.site.register(models.AvailableTime)