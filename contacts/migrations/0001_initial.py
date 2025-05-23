# Generated by Django 4.2.18 on 2025-02-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                ("organization", models.CharField(max_length=256, null=True)),
                ("email", models.EmailField(max_length=256)),
                ("phone", models.CharField(max_length=20)),
                (
                    "contactMethod",
                    models.CharField(
                        choices=[
                            ("email", "Email"),
                            ("text", "Text"),
                            ("phone", "Phone"),
                            ("whatsapp", "Whatsapp"),
                        ]
                    ),
                ),
                ("msg", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
