from django.contrib.auth.models import User
from django.db import models


class Ad(models.Model):
    """An advertisement submitted to be displayed on the site"""
    # The ad's owner
    owner = models.ForeignKey(User)

    # The ad's information
    image = models.ImageField()
    adult = models.BooleanField(default=False)
    destination = models.URLField(max_length=4096)


class AdLifecycle(models.Model):
    """A lifecycle for a given ad."""
    # The admin scheduling the ad
    admin_contact = models.ForeignKey(User)

    # The ad to be shown
    ad = models.ForeignKey(Ad)

    # Information about the lifecycle
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    paid = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Information about the ad's activity
    impressions = models.PositiveIntegerField(default=0)
    interactions = models.PositiveIntegerField(default=0)
