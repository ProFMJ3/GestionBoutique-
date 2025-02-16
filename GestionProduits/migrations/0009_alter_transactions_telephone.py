# Generated by Django 4.2.18 on 2025-02-16 04:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionProduits', '0008_transactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='telephone',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Le numéro doit être au format international (+123456789)', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
