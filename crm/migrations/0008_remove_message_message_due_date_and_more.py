# Generated by Django 4.1.3 on 2022-12-13 00:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_remove_message_message_files_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_due_date',
        ),
        migrations.AddField(
            model_name='message',
            name='message_due_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='message_processed',
            field=models.BooleanField(default=False),
        ),
    ]
