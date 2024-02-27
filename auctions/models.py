
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.categoryName}"


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageURL = models.CharField(max_length=1000)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name="listing_watchlist")

    def __str__(self):
        return f"{self.title}"
