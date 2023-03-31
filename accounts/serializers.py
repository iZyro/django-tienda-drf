from .models import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, logout, authenticate

# User Serializer
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(
        min_length=8,
        error_messages={'min_length': 'La contraseña debe tener al menos 8 caracteres.'},
        style={'class': 'form-control', 'input_type': 'password'}, 
        write_only=True,
        )    
    password2 = serializers.CharField(
        style={'class': 'form-control', 'input_type': 'password'}, 
        write_only=True,
        )
    

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def validate(self, data):
        username = data['username']
        email = data['email']
        password = data['password']
        password2 = data['password2']

        if password != password2:
            raise serializers.ValidationError('Las contraseñas no coinciden.')
        if username and User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return data
    
        
class ResetPasswordSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error':'Datos incorrectos'})