# Generated by Django 4.2.4 on 2023-09-04 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания'),
        ),
    ]