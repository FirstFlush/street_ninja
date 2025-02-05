# Generated by Django 4.2.18 on 2025-02-04 07:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0019_toilet_is_wheelchair_toilet_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="PublicWifi",
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
                ("ssid", models.CharField(max_length=256)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("is_active", models.BooleanField(default=True)),
                ("last_fetched", models.DateTimeField(null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
