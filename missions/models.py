from django.db import models
from common.models import TimeStampedModel


class Mission(TimeStampedModel):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='mission_images/', blank=True, null=True)
    points = models.IntegerField(blank=True, null=True, default=0)
    goal = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=30, choices=[
        ('initial', 'Initial'),
        ('basic', 'Basic'),
        ('advanced', 'Advanced'),        
        ('vip', 'VIP'),        
    ], default='basic')
    status = models.CharField(max_length=30, choices=[
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted')
    ], default='active')
    finished_times = models.IntegerField(blank=True, null=True, default=0)

    rewards = models.ManyToManyField('rewards.Reward', related_name='mission_rewards', blank=True)


    def __str__(self):
        return self.title
