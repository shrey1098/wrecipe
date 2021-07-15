from django.db import models
from django.contrib.auth.models import User, AbstractUser


class recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, unique=False)
    timestamp = models.DateField(auto_now_add=True)
    visibilityTypes = (
        ('PR', 'Private'),
        ('PU', 'Public'),
    )
    visibilityType = models.CharField(choices=visibilityTypes, max_length=20, default='Public')
    recipeTypes = (
        ('V', 'Vegetarian'),
        ('NV', 'Non-Vegetarian'),
        ('VE', 'Vegan'),
    )
    recipeType = models.CharField(choices=recipeTypes, max_length=20)
    mealTypes = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('S', 'Snack'),
        ('DE', 'Dessert'),
    )
    mealType = models.CharField(choices=mealTypes, max_length=20)
    servingSize = models.PositiveSmallIntegerField()
    cookingTime = models.PositiveIntegerField()
    steps = models.JSONField()
    picture = models.URLField(default='https://raw.githubusercontent.com/shrey1098/img/main/462773.jpg')

    class Meta:
        unique_together = ("name", "steps", "picture")

    def __str__(self):
        return self.name


class viewedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeName = models.ForeignKey(recipe, on_delete=models.CASCADE)


class likedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeName = models.ForeignKey(recipe, on_delete=models.CASCADE)


class savedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeName = models.ForeignKey(recipe, on_delete=models.CASCADE)


class ingredientsList(models.Model):
    ingredient = models.CharField(max_length=100)
    hindi_name = models.CharField(max_length=200, blank=True)
    path = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient


class userIngredients(models.Model):
    ingredient = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.ingredient
