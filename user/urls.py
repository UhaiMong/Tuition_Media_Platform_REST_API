from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
router.register(r'profile_view', views.UserProfileViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('register/',views.UserRegistrationApiView.as_view(),name='register'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('activate/<uid64>/<token>',views.activate,name='activate'),
]