from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Product, Review, Customer
from .forms import ProductUpdateForm, ReviewForm


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
        return JsonResponse({'likes': product.likes})

    return redirect('eccomerce:product_detail', pk=product.pk)


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('eccomerce:product-detail', pk=product.pk)
    else:
        form = ProductUpdateForm(instance=product)

    return render(request, 'ecomerce/update_product.html', {'form': form, 'product': product})


def index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ecomerce/product-list.html', {'page_obj': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'ecomerce/product-details.html', {'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('eccomerce:product-list')

    return render(request, 'ecomerce/delete_product.html', {'product': product})


def customers(request):
    customers_list = Customer.objects.all()
    return render(request, 'ecomerce/customers.html', {'customers': customers_list})


def customer_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'ecomerce/customer-details.html', {'customer': customer})


class CreateProduct(CreateView):
    model = Product
    template_name = 'ecomerce/product-list.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('eccomerce:product-list')


class FoobarDetailView(DetailView):
    template_name = 'ecomerce/product-details.html'
    model = Product
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
