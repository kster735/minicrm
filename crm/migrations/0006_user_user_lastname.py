# Generated by Django 4.1.3 on 2022-12-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_remove_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_lastname',
            field=models.CharField(max_length=255, null=True),
        ),
    ]