from .serializers import *
from .forms import *

from datetime import timedelta

from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return redirect('shop:dashboard')

        messages.error(request, "El usuario o contraseña son incorrectos.")
        return render(request, 'accounts/login.html', {"form": LoginForm})
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('shop:dashboard')
        return render(request, 'accounts/login.html', {"form": LoginForm})


class RegisterView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('shop:dashboard')
        context = {
            "form": RegisterForm,
            "serializer": RegisterSerializer()
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Te has registrado correctamente.")
            return redirect("accounts:login")
        else:
            error_message = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_message.append(error)

            if error_message:
                messages.error(request, error_message[0])
                return redirect('accounts:register')
        form = RegisterForm(request.POST)
        form.save()



        
class Logout(APIView):
    def get(self,request, format = None):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
            logout(request)
        return redirect('accounts:login')
    
class ResetPasswordView(APIView):

    def get(self, request, *args, **kwargs):
        form = ForgotPasswordForm(user=request.user)
        return render(request, 'accounts/reset_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            password_reset_token = PasswordResetToken.objects.get(token=token)
            if timezone.now() > password_reset_token.expires_at:
                print("time test")
                messages.error(request, "El enlace para restablecer la contraseña ha caducado, por favor, solicite un nuevo enlace.")
                return redirect('accounts:reset_password')
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
            if default_token_generator.check_token(user, token):
                form = ForgotPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "La contraseña ha sido cambiada correctamente.")
                    return redirect('accounts:login')
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f'Error en {field}: {error}')
        except:
            print('except error')
            pass
        return redirect(f'http://localhost:8000/reset_password/{uidb64}/{token}/')
    
class ForgotPassword(APIView):
    def get(self, request):
        return render(request, 'accounts/forgot_password.html')

    def post(self, request):
        data = request.POST['data']
        try:
            user = User.objects.get(Q(username=data) | Q(email=data))
        except:
            messages.error(request, "Nombre de usuario o email no encontrados.")
            return redirect('accounts:forgot_password')

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        print(f"uid: {uidb64}  token: {token}")
        expires_at = timezone.now() + timedelta(hours=1)  # Establecer el tiempo límite en 24 horas
        password_reset_token = PasswordResetToken(user=user, token=token, expires_at=expires_at)
        password_reset_token.save()
            

        link= f'http://localhost:8000/reset_password/{uidb64}/{token}/'
        print(link)
        return render(request, 'accounts/recovery_password.html', {'link': link})

        # CUANDO EXISTA EL SERVIDOR SMTP
        #messages.success(request, "Se ha enviado un mensaje a tu email para recuperar la cuenta.")
        #return redirect('accounts:login')