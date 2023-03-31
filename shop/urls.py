from .views import *
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('category/<category>', CategoryView.as_view(), name='category'),
    path('product/<id>', ProductView.as_view(), name='product'),
    path('favorite/<id>', FavoriteView.as_view(), name='favorite'),
    path('favorite_list/', FavoriteList.as_view(), name='favorite_list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart_remove/<user>/<id>', CartRemove.as_view(), name='cart_remove'),
    path('account/', AccountView.as_view(), name='account'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('checkout/', CheckoutView.as_view(), name='checkout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)