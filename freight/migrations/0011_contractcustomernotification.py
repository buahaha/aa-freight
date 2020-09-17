# Generated by Django 2.2.5 on 2019-11-27 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("freight", "0010_auto_20191108_2220"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContractCustomerNotification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("outstanding", "outstanding"),
                            ("in_progress", "in progress"),
                            ("finished_issuer", "finished issuer"),
                            ("finished_contractor", "finished contractor"),
                            ("finished", "finished"),
                            ("canceled", "canceled"),
                            ("rejected", "rejected"),
                            ("failed", "failed"),
                            ("deleted", "deleted"),
                            ("reversed", "reversed"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "date_notified",
                    models.DateTimeField(help_text="datetime of notification"),
                ),
                (
                    "contract",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="freight.Contract",
                    ),
                ),
            ],
            options={
                "unique_together": {("contract", "status")},
            },
        ),
    ]
