from django.shortcuts import render,redirect
from first_app.models import pet
from .models import Cart
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F,Sum


# Create your views here.
def add_to_cart(request,id):
    cart_id = request.session.session_key
    Pet = pet.objects.get(id=id)
    cart = Cart.objects.filter(Pet__id = Pet.id,user = request.user)

    if cart.exists():
        messages.warning(request,"Item alreday in cart!!!")
        return redirect("/")
    else:
        if cart_id == None:
            cart_id = request.session.create()
    
        Price = Pet.price
        User = request.user

        Cart(cart_id = cart_id,Pet=Pet,user=User,totalprice = Price).save()

        messages.success(request,"Item added in cart successfully")
        return redirect("/")

def show_all_cart_view(request):
    if request.user.is_authenticated:
        crt_data = Cart.objects.filter(user = request.user)
        flag = crt_data.exists()
        all_crt_data = {
        'items':crt_data,
        'flag':flag
    }
        return render(request,'cart/cart-list.html',all_crt_data)
    else:
        return redirect('login_page')
    # crt_data = Cart.objects.filter(user = request.user)
    # flag = crt_data.exists()

    # all_crt_data = {
    #     'items':crt_data,
    #     'flag':flag
    # }

    # return render(request,'cart/cart-list.html',all_crt_data)

def update_cart(request,id):
    p = request.POST.get('price')
    q = request.POST.get('qnt')
    p_id = request.POST.get('id') 
    totalPrice = float(p) * int(q)
    Cart.objects.filter(id=p_id).update(quantity =q,totalprice = totalPrice)
    total_amount = Cart.objects.filter(user = request.user).aggregate(total = Sum('totalprice'))['total'] or 0.0
    return JsonResponse({'status': True,'totalprice':totalPrice,'totalam':total_amount})

def delete_view(request,id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    messages.success(request,"Item deleted from cart successfully")
    return redirect('all_data_cart')