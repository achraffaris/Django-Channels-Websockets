# Generated by Django 4.0.2 on 2022-02-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.TextField(default='anonym'),
        ),
    ]
