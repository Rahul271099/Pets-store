# Generated by Django 4.2.1 on 2023-05-30 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_pet_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='image',
            field=models.ImageField(default=None, upload_to='media'),
        ),
    ]
