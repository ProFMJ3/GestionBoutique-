# Generated by Django 4.2.18 on 2025-02-16 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionProduits', '0007_remove_panier_nouveaunomclient_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operateur', models.CharField(choices=[('Moov', 'Moov'), ('Yas', 'Yas')])),
                ('operation', models.CharField(choices=[('Retrait', 'Retrait'), ('Dépot', 'Dépot')])),
                ('montant', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('dateTransaction', models.DateTimeField(auto_now_add=True, null=True)),
                ('telephone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='GestionProduits.client')),
            ],
        ),
    ]
