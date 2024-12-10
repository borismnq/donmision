# Generated by Django 5.1.3 on 2024-11-09 08:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("missions", "0001_initial"),
        ("organizations", "0001_initial"),
        ("users", "0002_user_address_user_age_user_created_at_user_gender_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserOrganization",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("collaborator", "Collaborator"),
                            ("follower", "follower"),
                        ],
                        default="follower",
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                            ("deleted", "Deleted"),
                        ],
                        default="active",
                        max_length=50,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizations.organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserOrganizationMission",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("progress", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In Progress"),
                            ("finished", "Finished"),
                            ("cancelled", "Cancelled"),
                            ("deleted", "Deleted"),
                            ("expired", "Expired"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
                (
                    "mission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="missions.mission",
                    ),
                ),
                (
                    "user_organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.userorganization",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_organization", "mission")},
            },
        ),
        migrations.AddField(
            model_name="userorganization",
            name="missions",
            field=models.ManyToManyField(
                through="users.UserOrganizationMission", to="missions.mission"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="userorganization",
            unique_together={("user", "organization")},
        ),
    ]