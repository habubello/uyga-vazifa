import email.message
from email.message import EmailMessage

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Product, Review, Img, Customer


def product_saved(sender, instance, created, **kwargs):
    if created:
        users = Customer.objects.all()
        email_of_users = [user.email for user in users]
        email = EmailMessage(
            f'Product saved',
            f'{instance.name.title()} successfully saved',
            to=email_of_users
        )
        email.send()
        print('Email sent')

    else:
        users = Customer.objects.all()
        email_of_users = EmailMessage()
        email = EmailMessage(
            f'Product saved',
            f'{instance.name.title()} sucsessfully savded'
        )