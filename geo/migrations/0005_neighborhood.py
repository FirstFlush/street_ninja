# Generated by Django 4.2.18 on 2025-05-18 01:15

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0004_delete_inquirycount"),
    ]

    operations = [
        migrations.CreateModel(
            name="Neighborhood",
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
                ("name", models.CharField(max_length=256)),
                (
                    "boundary",
                    django.contrib.gis.db.models.fields.PolygonField(srid=4326),
                ),
                ("centroid", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
