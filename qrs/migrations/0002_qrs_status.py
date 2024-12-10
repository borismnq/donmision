# Generated by Django 5.1.3 on 2024-11-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qrs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="qrs",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("scanned", "Scanned"),
                    ("deleted", "Deleted"),
                ],
                default="pending",
                max_length=30,
            ),
        ),
    ]
