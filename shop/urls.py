from .views import *
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('category/<category>', CategoryView.as_view(), name='category'),
    path('product/<id>', ProductView.as_view(), name='product'),
    path('favorite/<id>', FavoriteView.as_view(), name='favorite'),
    path('favorite_list/', FavoriteList.as_view(), name='favorite_list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)