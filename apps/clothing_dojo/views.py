from django.shortcuts import render, redirect, HttpResponse
from apps.clothing_admin.models import *
from apps.clothing_dojo.models import *
from djangounchained_flash import ErrorManager, getFromSession

def index(request):
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()
    e=getFromSession(request.session['flash'])
    context={
        'products':Product.objects.all(),
        'cart_success':e.getMessages('cart_success')
    }
    request.session['flash']=e.addToSession()
    return render(request, 'clothing_dojo/clothingDojo_main.html', context)

def productPage(request, product_id):
    if len(Product.objects.filter(id=product_id))==0:
        print('Attempting to view product that does not exist')
        return redirect('/')
    context={
        'product':Product.objects.get(id=product_id),
        'other_products':Product.objects.exclude(id=product_id)[:4]
    }
    return render(request, 'clothing_dojo/clothingDojo_productPage.html', context)

def addToCart(request, product_id):
    if len(Product.objects.filter(id=product_id))==0:
        print('Attempting to view product that does not exist')
        return redirect('/')
    print('Adding item ', Product.objects.get(id=product_id).name, ' to cart.')
    e=getFromSession(request.session['flash'])
    string='Successfully added '+Product.objects.get(id=product_id).name+' to cart.'
    e.addMessage(string, 'cart_success')
    request.session['flash']=e.addToSession()
    return redirect('/')
