# Generated by Django 4.2.18 on 2025-02-03 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0011_foodprogram_program_population_served"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="foodprogram",
            name="last_updated",
        ),
        migrations.AddField(
            model_name="foodprogram",
            name="last_fetched",
            field=models.DateTimeField(null=True),
        ),
    ]
