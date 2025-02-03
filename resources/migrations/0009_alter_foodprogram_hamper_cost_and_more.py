# Generated by Django 4.2.18 on 2025-02-03 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0008_alter_foodprogram_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="foodprogram",
            name="hamper_cost",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="foodprogram",
            name="meal_cost",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="foodprogram",
            name="referral_email",
            field=models.EmailField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="foodprogram",
            name="signup_email",
            field=models.EmailField(max_length=256, null=True),
        ),
    ]
