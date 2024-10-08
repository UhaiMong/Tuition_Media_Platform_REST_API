from django.shortcuts import render,redirect
from rest_framework import viewsets
from .import models
from .import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.exceptions import NotAuthenticated
# for token, uid generation
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.http import JsonResponse
# for email sending
from rest_framework.parsers import MultiPartParser,FormParser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class UserRegistrationApiView(APIView):
    serializer_class = serializers.UserRegistrationSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}"
            email_subject = "Please Activate your account."
            email_body = render_to_string('email_confirm.html',{'confirm_link':confirm_link,'first_name':user.first_name,'last_name':user.last_name})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return Response({"status":"success","message":"Please check your mail box to confirm account"},status=status.HTTP_201_CREATED)
        else:
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
# account activation function

def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return JsonResponse({'status':'success','message':'Account activation successful'})
    else:
        return JsonResponse({'status':'error','message':'Activation link is invalid'})
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserProfileSerializer
    
    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")
        return user.profile
    
class UserProfileViewSet(viewsets.ModelViewSet):
    parser_classes = [IsAuthenticated]
    queryset = models.Profile.objects.all()
    serializer_class = serializers.UserProfileNormalSerializer
    
class UserLoginApiView(APIView):
    # def post(self,request):
    #     serializer = serializers.UserLoginSerializer(data=self.request.data)
    #     if serializer.is_valid():
    #         username = serializer.validated_data['username']
    #         password = serializer.validated_data['password']
    #         user = authenticate(username=username,password=password)
            
    #         if user:
    #             token,_ = Token.objects.get_or_create(user=user)
    #             return Response({'token':token.key, 'user_id':user.id})
    #         else:
    #             return Response({'error':'Invalid Credential'})
    #     return Response(serializer.errors)
    
    # login with email address or username
    def post(self, request):
        print(request.data)
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            login(request,user)
            return Response({'token': token.key, 'user_id': user.id,'message':'success'})
        return Response(serializer.errors, status=400) 
            

# user logout

class UserLogoutApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return redirect('login')
        else:
            return Response({"message": "User is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)
    
    
