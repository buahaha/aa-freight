# Generated by Django 2.2.5 on 2019-10-15 12:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("freight", "0001_initial_new"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pricing",
            name="price_per_collateral_percent",
            field=models.FloatField(
                blank=True,
                default=None,
                help_text="Add-on price in % of collateral",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
