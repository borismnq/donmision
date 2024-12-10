from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import TimeStampedModel

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser, TimeStampedModel):
    status = models.CharField(max_length=30, choices=[
        ('active', 'Active'), ('inactive', 'Inactive')
        , ('deleted', 'Deleted')
    ], default='active')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=30,blank=True, null=True)
    level = models.IntegerField(blank=True, null=True, default=1)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = "email"
    objects = UserManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.is_staff

    @property
    def is_active(self):
        return True if self.status=='active' else False

    def __str__(self):
        return self.email

class UserOrganization(TimeStampedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('collaborator', 'Collaborator'), ('follower', 'follower')], default='follower')
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('deleted', 'Deleted')], default='active')
    missions = models.ManyToManyField('missions.Mission', through='UserOrganizationMission')


    class Meta:
        unique_together = [['user', 'organization']]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name}"

class UserOrganizationMission(TimeStampedModel):
    user_organization = models.ForeignKey(UserOrganization, on_delete=models.CASCADE)
    mission = models.ForeignKey('missions.Mission', on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
        ('deleted', 'Deleted'),
        ('expired', 'Expired')
    ], default='pending')


    class Meta:
        unique_together = [['user_organization', 'mission']]

    def __str__(self):
        return f"{self.user_organization.user.email} - {self.mission.title}"