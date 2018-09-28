from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products': products})


@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        url = request.POST['url']
        icon = request.FILES['icon']
        image = request.FILES['image']

        if title and body and url and icon and image:
            product = Product()
            product.title = title
            product.body = body
            if url.startswith('http://') or url.startswith('https://'):
                product.url = url
            else:
                product.url = 'http://' + url
            product.icon = icon
            product.image = image
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html',
                          {'error': 'All fields are required'})
    else:
        return render(request, 'products/create.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})


@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
