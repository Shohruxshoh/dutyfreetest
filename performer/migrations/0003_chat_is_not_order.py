# Generated by Django 5.1 on 2024-09-16 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performer', '0002_chat_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_not_order',
            field=models.BooleanField(default=True),
        ),
    ]
