# Generated by Django 5.1.3 on 2024-11-15 04:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0001_initial"),
        ("rewards", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reward",
            name="organization",
            field=models.ForeignKey(
                default=6,
                on_delete=django.db.models.deletion.CASCADE,
                to="organizations.organization",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="reward",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Active"),
                    ("inactive", "Inactive"),
                    ("deleted", "Deleted"),
                ],
                default="active",
                max_length=30,
            ),
        ),
    ]