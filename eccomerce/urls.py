from django.urls import path

from . import views
from .views import index

app_name = 'eccomerce'

urlpatterns = [
    path('', index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('customers/<str:customer_name>/', views.customer_details, name='customer_details'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('like/<int:pk>/', views.like_product, name='like_product'),
    path('reviews/<int:pk>/', views.show_reviews, name='reviews'),
    path('add-review/<int:pk>/', views.add_review, name='add_review'),
    path('reviews/<int:pk>/', views.show_reviews, name='reviews'),
    path('customers/', views.customers, name='customers'),

]

