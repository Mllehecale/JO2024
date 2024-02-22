# Generated by Django 5.0.2 on 2024-02-22 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JoBooking', '0002_commande'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paiement', models.BooleanField(default=False)),
                ('date_commande', models.DateTimeField(blank=True, null=True)),
                ('commandes', models.ManyToManyField(to='JoBooking.commande')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
