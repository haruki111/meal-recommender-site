from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import (
    get_user_model
)
import math


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ', max_length=50)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    imageUrl = models.CharField(max_length=200)
    countryOfOrigin = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE, verbose_name='ユーザー')
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    dateAdded = models.DateTimeField(
        default=timezone.now
    )

    def avgRating(self):
        if self.numberOfVotes() == 0:
            return 0

        votes = MealRating.objects.filter(meal=self)

        total = 0
        for vote in votes:
            total += vote.rating

        return math.floor(total / self.numberOfVotes()*10)/10

    def totalRating(self):
        if not self.numberOfVotes():
            return 0

        votes = MealRating.objects.filter(meal=self)

        total = 0
        for vote in votes:
            total += vote.rating

        return float(total)

    def numberOfVotes(self):
        count = MealRating.objects.filter(meal=self).count()
        return count

    def __str__(self):
        return self.name


class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE, verbose_name='ユーザー')
    rating = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(5.00)],
    )
    dateOfRating = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.meal
