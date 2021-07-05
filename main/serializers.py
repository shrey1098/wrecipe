from rest_framework import serializers
from .models import recipe, savedRecipe, ingredientsList, userIngredients


class recipeMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = recipe
        fields = (
            'id', 'user_id', 'name', 'recipeType', 'cookingTime', 'picture', 'views',
        )


class recipeSerializer(serializers.ModelSerializer):
    class Meta:
        steps = serializers.JSONField
        model = recipe
        fields = "__all__"


class savedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = savedRecipe
        fields = "__all__"


class ingredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredientsList
        fields = "__all__"


class userIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = userIngredients
        fields = "__all__"
