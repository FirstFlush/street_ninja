# Generated by Django 4.2.18 on 2025-02-04 03:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0016_alter_drinkingfountain_in_operation"),
    ]

    operations = [
        migrations.CreateModel(
            name="Toilet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=256, null=True)),
                ("description", models.CharField(max_length=256, null=True)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("notes", models.TextField(null=True)),
                ("summer_hours", models.CharField(max_length=64, null=True)),
                ("winter_hours", models.CharField(max_length=64, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("last_fetched", models.DateTimeField(null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
