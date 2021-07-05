from django.contrib import admin
from .models import recipe, savedRecipe, ingredientsList, userIngredients


class recipeAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "timestamp", "visibilityType", "recipeType",
                    "mealType", "servingSize", "cookingTime", "views", "saves")


class savedRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "name")


class ingredientListAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "hindi_name", "path")


class userIngredientsAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "user")


admin.site.register(recipe, recipeAdmin)
admin.site.register(savedRecipe, savedRecipeAdmin)
admin.site.register(ingredientsList, ingredientListAdmin)
admin.site.register(userIngredients, userIngredientsAdmin)
