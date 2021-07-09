from django.contrib import admin
from .models import recipe, viewedBy, savedBy, likedBy, ingredientsList, userIngredients


class recipeAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "timestamp", "visibilityType", "recipeType",
                    "mealType", "servingSize", "cookingTime")


class savedRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipeName")


class viewRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipeName")


class likeRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipeName")


class ingredientListAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "hindi_name", "path")


class userIngredientsAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "count")


admin.site.register(recipe, recipeAdmin)
admin.site.register(viewedBy, viewRecipeAdmin)
admin.site.register(savedBy, savedRecipeAdmin)
admin.site.register(likedBy, likeRecipeAdmin)
admin.site.register(ingredientsList, ingredientListAdmin)
admin.site.register(userIngredients, userIngredientsAdmin)
