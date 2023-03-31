from .views import *
from django.urls import path

urlpatterns = [
    path('user/', UserList.as_view(), name='user_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('forgot_password/', ForgotPassword.as_view(),name='forgot_password'),
    path('recovery_password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='recovery_password'),

]