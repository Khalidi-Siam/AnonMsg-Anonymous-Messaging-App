# Generated by Django 5.2 on 2025-05-14 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture_encrypted',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture_nonce',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
