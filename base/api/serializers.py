

from rest_framework import serializers
from base.models import User,Image,PinataUpload,Role,Action,RoleAction
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password1 = serializers.CharField(write_only=True, required=True)

    
    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name','email','bName','brName','acNo','acTitle','password', 'password1',]

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            bName=validated_data['bName'],
            brName=validated_data['brName'],
            acNo=validated_data['acNo'],
            acTitle=validated_data['acTitle'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user_data = user
        print(user_data.bName)
        token = RefreshToken.for_user(user).access_token
        user = User.objects.get(email=user_data.email)
        print(user)
        relativeLink=reverse('email-verify')
        absurl = 'http://127.0.0.1:8000'+relativeLink+"?token="+str(token)
        email_body = 'Hi'+user.acTitle+' Use the link below to verify your email \n'+absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
        Util.send_email(data)
        print(token)

        return user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

        

class PinataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinataUpload
        fields = '__all__'


###################################################################

class RegisterNorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password1 = serializers.CharField(write_only=True, required=True)

    
    class Meta:
        model =  User
        fields = ['first_name','last_name','email','password', 'password1',]

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.is_norUser=True
        user.save()
        user_data = user
        token = RefreshToken.for_user(user).access_token
        user = User.objects.get(email=user_data.email)
        print(user)
        relativeLink=reverse('email-verify')
        absurl = 'http://127.0.0.1:8000'+relativeLink+"?token="+str(token)
        email_body = 'Hi, Use the link below to verify your email \n'+absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
        Util.send_email(data)
        print(token)

        return user




class RegisterBoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password1 = serializers.CharField(write_only=True, required=True)

    
    class Meta:
        model =  User
        fields = ['email','password', 'password1']

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_boUser=True
        user.save()
        user_data = user
        token = RefreshToken.for_user(user).access_token
        user = User.objects.get(email=user_data.email)
        print(user)
        # relativeLink=reverse('email-verify')
        # absurl = 'http://127.0.0.1:8000'+relativeLink+"?token="+str(token)
        # email_body = 'Hi, Use the link below to verify your email \n'+absurl
        # data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
        # Util.send_email(data)
        print(token)

        return user

class RoleSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


######################################################


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class RoleActionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = RoleAction
        fields ='__all__'# ['role','action'] #'id',
