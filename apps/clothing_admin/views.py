from django.shortcuts import render, redirect, HttpResponse
from apps.clothing_admin.models import *
from apps.clothing_dojo.models import *
from djangounchained_flash import ErrorManager, getFromSession

def index(request):
    return render(request, 'clothing_admin/admin_login.html')
    
def processLogin(request):
    if(request.method!='POST'):
        print('Invalid entry attempted')
        return redirect('/admin')
    print('Login attempted')
    print('Allowing access for now')
    return redirect('/admin/login/')

def login(request):
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()
    return redirect('/admin/orders/')

def logout(request):
    return redirect('/admin')

def orders(request):
    context={
        'orders':Order.objects.all().order_by('-created_at')
    }
    return render(request, 'clothing_admin/admin_orders.html', context)

def products(request):
    e=getFromSession(request.session['flash'])
    context={
        'product_success':e.getMessages('product_success'),
        'products':Product.objects.all()
    }
    request.session['flash']=e.addToSession()
    return render(request, 'clothing_admin/admin_products.html', context)

def addProduct(request):
    if 'description' not in request.session:
        request.session['description']=''
    if 'price' not in request.session:
        request.session['price']=''
        request.session['product_name']=''
        request.session['image_path']=''
        request.session['description']=''
    e=getFromSession(request.session['flash'])
    context={
        'product_name_errors':e.getMessages('product_name'),
        'product_name':request.session['product_name'],
        'image_path_errors':e.getMessages('image_path'),
        'image_path':request.session['image_path'],
        'price_errors':e.getMessages('price'),
        'price':request.session['price'],
        'color_errors':e.getMessages('color'),
        'description':request.session['description'],
        'description_errors':e.getMessages('description')
    }
    request.session['flash']=e.addToSession()
    return render(request, 'clothing_admin/admin_addNew.html', context)

def processNew(request):
    if(request.method!='POST'):
        return redirect('/admin')
    print('Recieved Data: ', request.POST)
    # print('Color: ',request.POST['color'])
    errors=Product.objects.validate(request.POST)
    e=getFromSession(request.session['flash'])
    if(len(request.POST['color_1'])==0):
            errors['color']='Product must have atleast one color'
    else:
        for i in range(2, int(request.POST['num_colors'])+1):
            if len(request.POST['color_'+str(i)])==0:
                e.addMessage('Color cannot be empty', 'color')
                break

    if(len(errors)):
        print('Errors: ', errors)
        for tag,error in errors.items():
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        request.session['product_name']=request.POST['product_name']
        request.session['image_path']=request.POST['image_path']
        request.session['price']=request.POST['price']
        request.session['description']=request.POST['description']
        return redirect('/admin/addProduct/')
    
    colors=[]
    for i in range(1, int(request.POST['num_colors'])+1):
        color=Color(name=request.POST['color_'+str(i)])
        color.save()
        colors.append(color)

    p=Product(name=request.POST['product_name'], cost=request.POST['price'], image_path=request.POST['image_path'], description=request.POST['description'])
    p.save()
    # print('P-id',p.id)
    # Product.objects.create(name=request.POST['product_name'], cost=request.POST['price'], image_path=request.POST['image_path'])
    # for i in range(0, len(colors)):
    for color in colors:
        color.product=Product.objects.get(id=p.id)
        color.save()
        # p.colors.add(colors[i])
    request.session['product_name']=''
    request.session['image_path']=''
    request.session['price']=''
    request.session['description']=''
    e.addMessage('Product successfully added', 'product_success')
    request.session['flash']=e.addToSession()
    
    return redirect('/admin/products/')
    
def deleteProduct(request, product_id):
    print('Deleting product ', product_id)
    if(len(Product.objects.filter(id=product_id))==0):
        print('Attempting to delete product that does not exist')
        return redirect('/admin/products/')
    p=Product.objects.get(id=product_id)
    p.delete()
    e=getFromSession(request.session['flash'])
    e.addMessage('Product successfully deleted', 'product_success')
    request.session['flash']=e.addToSession()
    return redirect('/admin/products/')

def editProduct(request, product_id):
    if(len(Product.objects.filter(id=product_id))==0):
        print('Attempting to edit product that does not exist')
        return redirect('/admin/products/')
    e=getFromSession(request.session['flash'])
    p=Product.objects.get(id=product_id)
    context={
        'product_name_errors':e.getMessages('product_name'),
        'image_path_errors':e.getMessages('image_path'),
        'price_errors':e.getMessages('price'),
        'color_errors':e.getMessages('color'),
        'description_errors':e.getMessages('description'),
        'product':p,
        'colors':p.colors.all(),
        'num_colors':len(p.colors.all())
    }
    request.session['flash']=e.addToSession()
    return render(request, 'clothing_admin/admin_editProduct.html', context)

def processEdit(request, product_id):
    if(request.method!='POST'):
        return redirect('/admin/products/')
    if(len(Product.objects.filter(id=product_id))==0):
        print('Attempting edit on product that doesn\'t exist')
        return redirect('/admin/products/')
    print('Processing edit')
    print('Request: ', request.POST)
    colors=request.POST.getlist('color')
    print(colors)
    e=getFromSession(request.session['flash'])
   
    errors=Product.objects.validate(request.POST)
    # if(len(colors[0])==0):
    #     errors['color']='Product must have atleast one color'
    if(len(colors)==0):
        errors['color']='Product must have atleast one color'
    for i in range(1, int(request.POST['num_colors'])):
        if len(colors[i])==0:
            errors['color']='Color cannot be empty'
            break

    if(len(errors)):
        print('Errors: ', errors)
        for tag,error in errors.items():
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        return redirect('/admin/edit/'+str(product_id)+'/')

    p=Product.objects.get(id=product_id)
    p.name=request.POST['product_name']
    p.image_path=request.POST['image_path']
    p.price=request.POST['price']
    p.description=request.POST['description']
    # UPDATE COLORS OF P
    p.colors.clear()
    color_objects=[]
    for color in colors:
        color_objects.append(Color.objects.create(name=color))
    for color in color_objects:
        color.product=Product.objects.get(id=product_id)
        color.save()
    p.save()

    e.addMessage('Product successfully edited!', 'product_success')
    request.session['flash']=e.addToSession()
    return redirect('/admin/products/')

def orderInfo(request, order_id):
    if len(Order.objects.filter(id=order_id))==0:
        print('Attempting to view order that does not exist')
        return redirect('/admin/orders/')
    print('Looking at order')
    context={
        'order':Order.objects.get(id=order_id),
    }
    return render(request, 'clothing_admin/admin_orderInfo.html', context)

def changeStatusAPI(request, order_id):
    if(request.method!='POST'):
        return redirect('/admin/orders/')
    if(len(Order.objects.filter(id=order_id))==0):
        return redirect('/admin/orders/')
    o=Order.objects.get(id=order_id)
    o.status=request.POST['status']
    o.save()
    print(o.status)
    return HttpResponse('Correctly Changed Status')

def batchInfo(request):
    e=getFromSession(request.session['flash'])
    context={
        'locations':Location.objects.all(),
        'batch_success':e.getMessages('batch_success')
    }
    request.session['flash']=e.addToSession()
    return render(request, 'clothing_admin/admin_batchInfo.html', context)

def viewLocation(request, location_id):
    if len(Location.objects.filter(id=location_id))==0:
        print('Attempting to access location that does not exist')
        return redirect('/admin/batchInfo/')
    if len(Location.objects.get(id=location_id).batches.all())==0:
        Batch.objects.create(location=Location.objects.get(id=location_id))
    context={
        'location':Location.objects.get(id=location_id),
        'batches':Location.objects.get(id=location_id).batches.all().order_by('-created_at')
    }
    return render(request, 'clothing_admin/admin_viewLocation.html', context)

def viewBatch(request, batch_id):
    if len(Batch.objects.filter(id=batch_id))==0:
        print('Attempting to access batch that does not exist')
        return redirect('/admin/batchInfo/')
    batch_total=0
    b=Batch.objects.get(id=batch_id)
    for item in b.items.all():
        batch_total+=item.total
    context={
        'batch':Batch.objects.get(id=batch_id),
        'items':Batch.objects.get(id=batch_id).items.all().order_by('product','color'),
        'batch_total':batch_total
    }
    return render(request,'clothing_admin/admin_viewBatch.html', context)

def batchConfirm(request, batch_id):
    if len(Batch.objects.filter(id=batch_id))==0:
        print('Attempting to access location that does not exist')
        return redirect('/admin/batchInfo/')
    context={
        'batch':Batch.objects.get(id=batch_id)
    }
    return render(request,'clothing_admin/admin_batchConfirm.html', context)

def finalizeBatch(request, batch_id):
    if len(Batch.objects.filter(id=batch_id))==0:
        print('Attempting to access location that does not exist')
        return redirect('/admin/batchInfo/')
    if(Batch.objects.get(id=batch_id).status=='Closed'):
        print('This batch is already closed')
        return redirect('/admin/batchInfo/')
    
    b=Batch.objects.get(id=batch_id)
    b.status='Closed'
    b.save()
    location=Batch.objects.get(id=batch_id).location
    Batch.objects.create(location=location)
    e=getFromSession(request.session['flash'])
    e.addMessage('Batch successfully finalized', 'batch_success')
    request.session['flash']=e.addToSession()
    print('Batch successfully finalized')
    string='/admin/batchInfo/viewLocation/'+str(location.id)+'/'
    return redirect(string)

def test(request):
    return render(request, 'clothing_admin/test.html')

def processTest(request):
    print(request.POST)
    return redirect('/admin/test/')
