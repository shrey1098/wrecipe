from rest_framework import serializers
from .models import recipe, savedRecipe


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
