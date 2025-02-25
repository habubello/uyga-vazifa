from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Product, Review, Img, Customer


@receiver(pre_save, sender=Product)
def update_stock_status(sender, instance, **kwargs):
    instance.stock = instance.quantity > 0


@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    if created:
        print(f"Создан новый продукт: {instance.name}")
    else:
        print(f"Обновлён продукт: {instance.name}")


@receiver(post_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    images = Img.objects.filter(product=instance)
    for img in images:
        img.image.delete(save=False)
    images.delete()


@receiver(post_save, sender=Review)
def notify_new_review(sender, instance, created, **kwargs):
    if created:
        print(f"Новый отзыв на {instance.product.name} от {instance.name}: {instance.review}")


@receiver(post_save, sender=Customer)
def log_customer_creation(sender, instance, created, **kwargs):
    if created:
        print(f"Зарегистрирован новый клиент: {instance.name} ({instance.email})")
