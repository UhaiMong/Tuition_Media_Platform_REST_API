from django.shortcuts import render
from .import models
from rest_framework import viewsets,filters,pagination
from .import serializers
# from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class AvailableTimeForSpecificTutor(filters.BaseFilterBackend):
    def filter_queryset(self,request,query_set,view):
        tutor_id = request.query_params.get('tutor_id')
        if tutor_id:
            return query_set.filter(tuition = tutor_id)
        return query_set

class AvailableTimeViewSet(viewsets.ModelViewSet):
    queryset = models.AvailableTime.objects.all()
    serializer_class = serializers.AvailableTimeSerializer
    filter_backends = [AvailableTimeForSpecificTutor]
class TuitionPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = page_size
    max_page_size = 100
class TuitionViewSet(viewsets.ModelViewSet):
    queryset = models.Tuition.objects.all()
    serializer_class = serializers.TuitionSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = TuitionPagination
    search_fields = []
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    
class TuitionReviewViewSet(viewsets.ModelViewSet):
    queryset = models.TuitionReview.objects.all()
    serializer_class = serializers.TuitionReviewSerializer