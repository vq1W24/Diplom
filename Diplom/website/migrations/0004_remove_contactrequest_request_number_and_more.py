# Generated by Django 5.1.5 on 2025-01-31 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_contactrequest_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactrequest',
            name='request_number',
        ),
        migrations.RemoveField(
            model_name='contactrequest',
            name='status',
        ),
    ]
