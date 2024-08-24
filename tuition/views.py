from django.shortcuts import render
from .import models
from rest_framework import viewsets
from .import serializers

# Create your views here.

class TuitionViewSet(viewsets.ModelViewSet):
    queryset = models.Tuition.objects.all()
    serializer_class = serializers.TuitionSerializer
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    
class TuitionReviewViewSet(viewsets.ModelViewSet):
    queryset = models.TuitionReview.objects.all()
    serializer_class = serializers.TuitionReviewSerializer