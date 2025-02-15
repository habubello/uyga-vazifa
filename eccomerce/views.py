from django.core.paginator import Paginator

import eccomerce
from .models import Customer
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductUpdateForm,ReviewForm
from .models import Product, Review


def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('eccomerce:reviews', pk=product.pk)
    else:
        form = ReviewForm()

    return render(request, 'ecomerce/add_review.html', {'form': form, 'product': product})

def show_reviews(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    return render(request, 'ecomerce/reviews.html', {'reviews': reviews, 'product': product})






def like_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.likes += 1
        product.save()

    return redirect('eccomerce:product_detail', pk=product.pk)



def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('eccomerce:product_detail', pk=product.id)
    else:
        form = ProductUpdateForm(instance=product)

    return render(request, 'ecomerce/update_product.html', {'form': form, 'product': product})




def index(request):
        products = Product.objects.all()  # Получаем все товары
        paginator = Paginator(products, 10)  # Разбиваем на страницы по 10 товаров
        page_number = request.GET.get('page')  # Получаем номер страницы из запроса
        page_obj = paginator.get_page(page_number)  # Получаем объекты для нужной страницы

        return render(request, 'ecomerce/product-list.html', {'page_obj': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'ecomerce/product-details.html', {'product': product})



def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('eccomerce:product_list')

    return render(request, 'ecomerce/delete_product.html', {'product': product})




def customers(request):
    customers_list = Customer.objects.all()
    return render(request, 'ecomerce/customers.html', {'customers': customers_list})



def customer_details(request, customer_name):
    customer = get_object_or_404(Customer, name=customer_name)
    return render(request, 'ecomerce/customer-details.html', {'customer': customer})
