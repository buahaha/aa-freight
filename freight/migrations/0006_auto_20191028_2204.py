# Generated by Django 2.2.5 on 2019-10-28 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("freight", "0005_auto_20191028_2155"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contracthandler",
            name="organization",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="freight.EveOrganization",
            ),
        ),
    ]
