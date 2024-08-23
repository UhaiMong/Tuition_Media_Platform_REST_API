from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
router.register(r'list', views.TuitionViewSet)
router.register(r'application', views.ApplicationViewSet)
router.register(r'review', views.TuitionReviewViewSet,basename='review')
urlpatterns = [
    path('',include(router.urls))
]