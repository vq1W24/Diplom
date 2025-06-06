# Generated by Django 5.1.5 on 2025-01-29 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_contactrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactrequest',
            name='status',
            field=models.CharField(choices=[('new', 'Новая'), ('in_progress', 'В обработке'), ('completed', 'Завершена')], default='new', max_length=20, verbose_name='Статус'),
        ),
    ]
