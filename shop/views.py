from django.shortcuts import render, redirect

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

def dashboard(request):
    user = request.user
    context = {
        "user": user
    }
    return render(request, 'shop/dashboard.html', context)