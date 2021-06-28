from django.contrib import admin
from .models import recipe, savedRecipe


class recipeAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "timestamp", "visibilityType", "recipeType",
                    "mealType", "servingSize", "cookingTime", "views", "saves")


class savedRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "name")


admin.site.register(recipe, recipeAdmin)
admin.site.register(savedRecipe, savedRecipeAdmin)
