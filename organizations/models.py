from django.db import models
from common.models import TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    created_by = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    plan = models.CharField(max_length=50, choices=[('free', 'Free'), ('basic', 'Basic'), ('premium', 'Premium')], default='free')
    status = models.CharField(max_length=30, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('deleted', 'Deleted')], default='active')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)
