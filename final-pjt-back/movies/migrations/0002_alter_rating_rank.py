# Generated by Django 3.2.9 on 2021-11-21 08:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rank',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
