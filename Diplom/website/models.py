from django.db import models
import uuid
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class ContactRequest(models.Model):

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('awaiting_documents', 'Ожидает документы'),
        ('review', 'На проверке'),
        ('completed', 'Завершена'),
        ('rejected', 'Отклонена'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = PhoneNumberField(region="RU", verbose_name="Телефон")
    email = models.EmailField(verbose_name="Почта", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    file = models.FileField(
        upload_to='contact_requests/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Файл"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = "Контактная заявка"
        verbose_name_plural = "Контактные заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_number} - {self.full_name}"

    def update_status(self, new_status, save=True):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            if save:
                self.save()
        else:
            raise ValueError(f"Неверный статус: {new_status}")




class FNSNews(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    summary = models.TextField(verbose_name="Краткое содержание")
    link = models.URLField(verbose_name="Ссылка на новость")
    published = models.DateTimeField(verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новость ФНС"
        verbose_name_plural = "Новости ФНС"
        ordering = ['-published']

    def __str__(self):
        return self.title