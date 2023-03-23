from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from rest_framework.views import APIView

from .models import *
from .serializers import *

class DashboardView(TemplateView):
    template_name = 'shop/dashboard.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = request.user
        context['products'] = Product.objects.all()[:30]
        
        return self.render_to_response(context)
    

class CategoryView(TemplateView):
    template_name = 'shop/category.html'

    def get(self, request, *args, **kwargs):
        category = kwargs['category']

        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category__name=category)[:20]
        context['category'] = category

        return self.render_to_response(context)
    

class ProductView(TemplateView):
    template_name = 'shop/product.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=kwargs['id'])
        
        if request.user.is_authenticated:
            context['user'] = request.user
            try:
                Favorite.objects.get(user = context['user'], product = context['product'])
                context['favorite'] = True
            except Favorite.DoesNotExist:
                context['favorite'] = False

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        cantidad = request.POST['cantidad']
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=kwargs['id'])
        
        if request.user.is_authenticated:
            context['user'] = request.user

            data = {'user': context['user'].id, 'product': context['product'].id, 'quantity': cantidad}
            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(reverse('shop:product', kwargs={'id': context['product'].id}))
            try:
                Favorite.objects.get(user = context['user'], product = context['product'])
                context['favorite'] = True
            except Favorite.DoesNotExist:
                context['favorite'] = False
            return self.render_to_response(context)
        return redirect('accounts:login')

class FavoriteView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            product = Product.objects.get(id=kwargs['id'])
            try:
                favorite = Favorite.objects.get(user_id = request.user.id, product_id = kwargs['id'])
                favorite.delete()        
                return HttpResponseRedirect(reverse('shop:product', kwargs={'id': product.id}))
            except Favorite.DoesNotExist:
                data = {'user': user.id, 'product': product.id}
                serializer = FavoriteSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return HttpResponseRedirect(reverse('shop:product', kwargs={'id': product.id}))
        return redirect('accounts:login')


class FavoriteList(TemplateView):
    template_name = 'shop/favorite_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['favorites'] = Favorite.objects.filter(user = request.user)

            return self.render_to_response(context)
        
        return redirect('accounts:login')



# 1. HACER QUE ENVIE UN MENSAJE CUANDO SE AGREGUE ALGO AL CARRITO
# 2. HACER LA PÁGINA DEL CARRITO
# 3. HACER LA PÁGINA PARA "COMPRAR AHORA"