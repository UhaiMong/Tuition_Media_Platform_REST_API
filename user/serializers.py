from django.contrib.auth.models import User
from rest_framework import serializers
from .import models

# login with email or username
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


# User profile handle to get data and update
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    class Meta:
        model = models.Profile
        fields = ['username','first_name','last_name','email','educational_qualification','mobileNumber','profileImage']
        
    def update(self,instance,validated_data):
        # Update user
        user_data = validated_data.pop('user',{})
        user = instance.user
        user.username = user_data.get('username',user.username)
        user.first_name = user_data.get('first_name',user.first_name)
        user.last_name = user_data.get('last_name',user.last_name)
        user.email = user_data.get('email',user.email)
        
        # update profile
        instance.educational_qualification = validated_data.get('educational_qualification',instance.educational_qualification)
        instance.mobileNumber = validated_data.get('mobileNumber',instance.mobileNumber)
        instance.profileImage = validated_data.get('profileImage',instance.profileImage)
        
        return instance
        
# User registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error':"Password doesn't matched!"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':"Email already exist"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error':"That username is already exist."})
        # create account
        account = User(username=username,first_name=first_name,last_name=last_name,email=email)
        account.set_password(password)
        account.is_active=False
        account.save()
        profile = models.Profile.objects.create(user=account)
        print("Created Profile: ",profile.user.username)
        return account
    
class UserProfileNormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'
        
# Login
class UserLoginSerializer(serializers.Serializer):
    # username = serializers.CharField(required=True)
    # password = serializers.CharField(required=True)
   
    # Identifying with email or username 
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        user = authenticate(username=identifier, password=password)
        if not user:
            user = authenticate(username=self.get_username_by_email(identifier), password=password)
        
        if not user:
            raise serializers.ValidationError(_('Invalid credentials, please try again.'))
        
        attrs['user'] = user
        return attrs
    
    def get_username_by_email(self, email):
        try:
            user = User.objects.get(email=email)
            return user.username
        except User.DoesNotExist:
            return None
    
