from rest_framework import serializers
from .import models


class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AvailableTime
        fields = '__all__'
class TuitionSerializer(serializers.ModelSerializer):
    available_time = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Tuition
        fields = '__all__'
        
class ApplicationSerializer(serializers.ModelSerializer):
    tuition = serializers.StringRelatedField(many=False)
    profile = serializers.StringRelatedField(many=False)
    time = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Application
        fields = '__all__'

class TuitionReviewSerializer(serializers.ModelSerializer):
    tuition = serializers.StringRelatedField(many=False)
    profile = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.TuitionReview
        fields = '__all__'