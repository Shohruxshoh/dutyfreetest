# Generated by Django 5.1 on 2024-09-16 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_alter_chatmessage_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_not_order',
            field=models.BooleanField(default=False),
        ),
    ]
