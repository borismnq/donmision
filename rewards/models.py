from django.db import models
from common.models import TimeStampedModel


class Reward(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='reward_images/', blank=True, null=True)
    type = models.CharField(max_length=30, choices=[('basic', 'Basic'),('product', 'Product'), ('badge', 'Badge'), ('coupon', 'Coupon')], default='basic')
    status = models.CharField(max_length=30, choices=[('active', 'Active'),('inactive', 'Inactive'),('deleted', 'Deleted')], default='active')



    def __str__(self):
        return self.title
