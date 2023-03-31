from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView

from accounts.models import *
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
                messages.success(request, '¡Se ha agregado "(x{}) {}" al carrito!'.format(cantidad, context['product'].name))
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


class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['user'] = request.user
            context['cart_items'] = Cart.objects.filter(user=request.user)
            context['cart_total'] = sum(item.product.price * item.quantity for item in context['cart_items'])
            return self.render_to_response(context)
        return redirect('accounts:login')


class CartRemove(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(id=kwargs['user'])
            if request.user == user:
                cart = Cart.objects.get(id=kwargs['id'])
                cart.delete()
                messages.success(request, f'Se eliminó "x({cart.quantity}) {cart.product.name}" del carrito correctamente.')
                return redirect('shop:cart')
            else:
                return redirect('shop:dashboard')
        return redirect('accounts:login')



class AccountView(TemplateView):
    template_name = 'shop/account.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = super().get_context_data(**kwargs)

            context['user'] = UserData.objects.get(username=request.user.username)

            return self.render_to_response(context)
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        User.objects.filter(username = request.user.username).update(
            first_name = request.POST['name'],
            last_name = request.POST['last_name']
        )
        UserData.objects.filter(username = request.user.username).update(
            name = request.POST['name'],
            last_name = request.POST['last_name'],
            country = request.POST['country'],
            city = request.POST['city'],
            address1 = request.POST['address1'],
            address2 = request.POST['address2']
        )
        return redirect('shop:account')

class EditProfileView(TemplateView):
    template_name = 'shop/edit_profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = super().get_context_data(**kwargs)

            context['user'] = UserData.objects.get(username = request.user.username)

            return self.render_to_response(context)
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username = request.user)
        if check_password(request.POST['password'], user.password):
            User.objects.filter(username = user.username).update(
                username = request.POST['username'],
                email = request.POST['email']
            )
            UserData.objects.filter(username = user.username).update(
                username = request.POST['username'],
                email = request.POST['email'],
                phone = request.POST['phone']
            )
            messages.success(request, 'Se ha cambiado la información correctamente.')
            return redirect('shop:account')
        else:
            messages.error(request, "La contraseña no es válida.")
            return redirect('shop:edit_profile')


class ResetPasswordView(TemplateView):
    template_name = 'shop/reset_password.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = super().get_context_data(**kwargs)

            return self.render_to_response(context)
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):

        user = request.user

        if not user.check_password(request.POST['current_password']):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('shop:reset_password')
        
        if request.POST['new_password'] != request.POST['confirm_password']:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
            return redirect('shop:reset_password')

        if len(request.POST['new_password']) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('shop:reset_password')

        user.set_password(request.POST['new_password'])
        user.save()

        messages.success(request, 'La contraseña fue cambiada correctamente.')
        return redirect('shop:account')


class CheckoutView(TemplateView):
    template_name = 'shop/checkout.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = UserData.objects.get(username = request.user.username)
        context['cart_items'] = Cart.objects.filter(user=request.user)
        context['cart_total'] = sum(item.product.price * item.quantity for item in context['cart_items'])

        return self.render_to_response(context)

