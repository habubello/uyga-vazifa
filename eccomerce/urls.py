from django.urls import path
from . import views

app_name = 'eccomerce'

urlpatterns = [
    path('', views.index, name='index'),




    path('category/<slug:slug>/', views.product_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),





    path('customers/', views.customers, name='customers'),
    path('customers/<int:pk>/', views.customer_details, name='customer_details'),
    path('product/create/', views.CreateProduct.as_view(), name='create_product'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('like/<int:pk>/', views.like_product, name='like_product'),
    path('reviews/<int:pk>/', views.show_reviews, name='reviews'),
    path('add-review/<int:pk>/', views.add_review, name='add_review'),
]
