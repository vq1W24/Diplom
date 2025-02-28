from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.contrib.auth.models import User


class ContactRequest(models.Model):
    request_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4, editable=False)

    # Расширенный список статусов
    STATUS_CHOICES = [
        ('new', 'Новая'),  # Новая заявка
        ('in_progress', 'В обработке'),  # Заявка находится в обработке
        ('awaiting_documents', 'Ожидает документы'),  # Новый статус: ожидание документов
        ('review', 'На проверке'),  # Новый статус: на проверке
        ('completed', 'Завершена'),  # Заявка завершена
        ('rejected', 'Отклонена'),  # Новый статус: отклонена
    ]

    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = PhoneNumberField(region="RU", verbose_name="Телефон")
    email = models.EmailField(verbose_name="Почта", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    file = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name="Файл")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    def __str__(self):
        return f"{self.request_number} - {self.full_name}"