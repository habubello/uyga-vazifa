from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User


# Сигнал для отправки приветственного письма новому пользователю
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Добро пожаловать!",
            message=f"Привет, {instance.email}! Спасибо за регистрацию.",
            from_email="no-reply@example.com",
            recipient_list=[instance.email],
            fail_silently=True,  # Избегаем ошибок, если SMTP не настроен
        )
        print(f"Отправлено приветственное письмо {instance.email}")


# Сигнал для логирования удаления пользователя
@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    print(f"Пользователь {instance.email} был удалён.")
