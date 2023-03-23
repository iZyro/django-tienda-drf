from django.contrib import admin
from .models import *

admin.site.register(CategoryShop)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(Cart)