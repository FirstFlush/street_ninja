# Generated by Django 5.1.4 on 2025-01-22 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_shelter_delete_shelters'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shelter',
            old_name='last_updated',
            new_name='last_fetched',
        ),
    ]
