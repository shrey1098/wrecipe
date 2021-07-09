from rest_framework import serializers
from .models import recipe, savedBy, ingredientsList, userIngredients, likedBy


class ChoiceField(serializers.ChoiceField):
    """
    overriding the inbuilt ChoiceField in serializers to GET and POST
    values of Choice fields instead of keys
    """

    # used in recipeMultipleSerializer and recipeSerializer

    def to_representation(self, value):
        if value == '' and self.allow_blank:
            return value
        return self._choices[value]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class recipeSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = recipe
        fields = (
            'id', 'name'
        )


class recipeMultipleSerializer(serializers.ModelSerializer):
    recipeType = ChoiceField(choices=recipe.recipeTypes)
    likes = serializers.SerializerMethodField('get_likes')
    isLiked = serializers.SerializerMethodField('get_is_liked')

    # Use this method for the custom field

    @staticmethod
    def get_likes(obj):
        liked = recipe.objects.get(name=obj)
        number_of_likes = liked.likedby_set.all().count()
        return number_of_likes

    def get_is_liked(self, obj):
        liked = likedBy.objects.filter(recipeName=obj).values('user')
        user = self.validate_user()
        q = {'user': user}
        if q in liked:
            return True
        return False

    def validate_user(self):
        request = self.context.get('request')
        if request:
            return request.user.id

    class Meta:
        model = recipe
        fields = (
            'id', 'name', 'recipeType', 'cookingTime', 'picture', 'likes', 'isLiked',
        )


class recipeSerializer(serializers.ModelSerializer):
    recipeType = ChoiceField(choices=recipe.recipeTypes)

    class Meta:
        steps = serializers.JSONField
        model = recipe
        fields = "__all__"


class savedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = savedBy
        fields = "__all__"


class likedRecipeSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = likedBy
        fields = "__all__"


class ingredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredientsList
        fields = "__all__"


class ingredientListSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingredientsList
        fields = ("ingredient", "hindi_name")


class userIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = userIngredients
        fields = ('ingredient',)
