# Generated by Django 4.2.1 on 2023-06-19 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0007_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='price',
            field=models.FloatField(default='10'),
        ),
    ]
