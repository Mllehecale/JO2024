# Generated by Django 5.0.2 on 2024-02-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JoBooking', '0003_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='cle_paiement',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]