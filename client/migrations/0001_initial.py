# Generated by Django 5.1 on 2024-09-10 13:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Предлагаемая сумма')),
                ('city', models.CharField(blank=True, max_length=250, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=250, null=True, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=250, null=True, verbose_name='Дом')),
                ('structure', models.CharField(blank=True, max_length=250, null=True, verbose_name='Строение')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание заказа')),
                ('delivery', models.CharField(choices=[('1', 'До адреса'), ('2', 'По договорённости')], default='2', max_length=250, verbose_name='Доставка')),
                ('order_file', models.FileField(blank=True, null=True, upload_to='order_file/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказ',
            },
        ),
    ]
