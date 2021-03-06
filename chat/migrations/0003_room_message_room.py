# Generated by Django 4.0.2 on 2022-02-28 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_message_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='chat.room'),
            preserve_default=False,
        ),
    ]
