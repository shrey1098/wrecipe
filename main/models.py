from django.db import models
from django.contrib.auth.models import User


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
        ('V', 'Veg'),
        ('NV', 'Non-Veg'),
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
    picture = models.URLField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class savedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(recipe, on_delete=models.CASCADE)
