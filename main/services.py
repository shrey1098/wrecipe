from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from .serializers import recipeMultipleSerializer, recipeSerializerGet, ingredientListSerializer, \
    userIngredientsSerializer, recipeSearchSerializer, ingredientListSearchSerializer
from .models import recipe, savedBy, ingredientsList, userIngredients, likedBy, viewedBy


def getRecipesData(request):
    """
    *api url: /api.recipesdata* GET method only\n

    returns json of all recipes ordered from new to old.\n
    recipeMultipleSerializer takes context request as an argument as the serializer needs to check
    for request.user and cross check with likedRecipe model make new field isLiked.\n
    for return json fields check serializers.py
    :param request
    :return: json serialized list of all recipes
    """
    qs = recipe.objects.filter().order_by('-id')[:10]
    q = list(qs)
    serializer = recipeMultipleSerializer(q, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


def getRecipeData(user, recipeID):
    """
    *api url: /api.recipedata?id=*\n
    request takes recipe id as a header. Recipe is retrieved with the id.\n
    viewRecipe function checks if the user has viewed this recipe earlier or not, if not it creates a new entry to
    viewedBy model.\n
    All recipe fields are returned in the JSON response.\n
    :param user:
    :param recipeID:
    :return:
    """

    def viewRecipe():
        new_view, created = viewedBy.objects.get_or_create(user=user, recipeName_id=recipeID)
        if not created:
            pass

    try:
        qs = recipe.objects.get(pk=recipeID)
    except recipe.DoesNotExist:
        return Response('Recipe Does Not Exist')
    viewRecipe()
    serializer = recipeSerializerGet(qs)
    return Response(serializer.data, status=status.HTTP_200_OK)


def postRecipeData(serializer, user):
    """
    *api url: /api.recipedata*\n  POST method
    Validates the data sent by the user in the serializer.\n
    Capitalises the first letter of the name of the recipe\n
    saves the serializer
    :param serializer:
    :return: statusCode
    """
    #TODO Check Http Response for all requests
    if serializer.is_valid():
        if serializer.validated_data['user'] == user:
            serializer.validated_data['name'] = serializer.validated_data['name'].capitalize()
            serializer.save()
            return Response('Success', status=status.HTTP_201_CREATED)
        else:
            return Response('not allowed to post')
    return Response(serializer.errors)


def getSearchRecipe(query):
    """
    *api url: /api.recipesearch*\n
    \n
    GET Method only\n
    :param query:
    :return:  serialized JSON response of 10 recipes that contains substring query
    """
    qs = recipe.objects.filter(name__icontains=query)
    if qs is None:
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = recipeSearchSerializer(qs, many=True)
        return Response(serializer.data[:10], status=status.HTTP_200_OK)


def getUserRecipes(user):
    """
    *api url: api.userrecipesdata *\n
    :param user:
    :return: All recipes posted by a user
    """
    qs = recipe.objects.filter(user=user)
    serializer = recipeMultipleSerializer(qs.reverse(), many=True)
    return Response(serializer.data)


def likeOrUnlike(recipeID, user):
    """
     *api url:/api.likerecipe?id=*\n
     Checks if a user has liked the recipe or not, if yes the likedBy object is deleted else it is created\n
     Like and Unlike through one api url.\n
    :param recipeID:
    :param user:
    :return:Liked or unliked
    """
    new_like, created = likedBy.objects.get_or_create(recipeName_id=recipeID, user=user)
    if not created:
        new_like.delete()
        return Response('Unliked')
    else:
        return Response('Liked')


def getSavedRecipes(user):
    """
    *api url: /api.savedrecipesdata?id=*\n
    Gets all recipes saved by the user, which are not their own\n
    :param user:
    :return: JSON of all saved recipes
    """
    qs = recipe.objects.filter(savedby__user=user)
    serializer = recipeMultipleSerializer(qs, many=True)
    return Response(serializer.data)


def saveOrUnsave(recipeID, user):
    """
    *api url: /api.savedrecipesdata?id=*\n
    Saves the recipe for a user, also likes it at the same time.\n
    if already saved it deletes the savedBy object entry\n
    :param recipeID:
    :param user:
    :return: Saved or Unsaved
    """
    new_save, created = savedBy.objects.get_or_create(recipeName_id=recipeID, user=user)
    if not created:
        new_save.delete()
        likeOrUnlike(recipeID, user)
        return Response('Unsaved')
    else:
        likeOrUnlike(recipeID, user)
        return Response('Saved')


def postDeleteRecipe(recipeID, user):
    """
    *api url: api.deleterecipe?id=*\n
    Deletes a recipe where the user of the recipe and user of the request is the same.
    :param recipeID:
    :param user:
    :return: Deleted Successfully or Not Allowed
    """
    recipeUser = recipe.objects.filter(pk=recipeID).get().user
    if user == recipeUser:
        recipe.objects.filter(pk=recipeID).delete()
        return Response({'Deleted Successfully'})
    else:
        return Response({'Not Allowed'})


def getSearchIngredient(query):
    """
    *api url:/api.ingredientsearch?q=*\n
    searches for both english name and hindi names of ingredients\n
    :param query:
    :return:JSON list of all matching queries
    """
    if len(query) > 0:
        qs = ingredientsList.objects.filter(ingredient__icontains=query) or ingredientsList.objects.filter(
            hindi_name__icontains=query)
        serializer = ingredientListSearchSerializer(qs, many=True)
        return Response(serializer.data[:5])
    else:
        return Response(None)


def getIngredient(ingredientID):
    """
    *api url: api.getingredients?id=*\n
    :param ingredientID:
    :return:
    """
    qs = ingredientsList.objects.get(pk=ingredientID)
    serializer = ingredientListSerializer(qs)
    return Response(serializer.data)


def postAddNewUserIngredients(serializer):
    """
    *api url: /api.adduseringredient *\n
    Serialized fields = user and ingredients\n
    sent in the body of the post request\n
    User given ingredient is saved and its count is SET TO 1, if already exists count increased by 1
    :param serializer:
    :return:
    """
    if serializer.is_valid():
        check_ingredient = serializer.validated_data['ingredient']
        try:
            userIngredients.objects.get(ingredient=check_ingredient)
            userIngredients.objects.filter(ingredient=check_ingredient).update(count=F('count') + 1)
            return Response(serializer.data)
        except userIngredients.DoesNotExist:
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors)


def getActionUserIngredients():
    """
    *api url: api.useringredientsaction*\n
    gets all user Ingredients.
    :return:
    """
    qs = userIngredients.objects.all()
    serializer = userIngredientsSerializer(qs, many=True)
    return Response(serializer.data)


def postActionUserIngredients(request, action):
    """
    *api url: api.useringredientsaction?action=add OR clear*\n
    Add new ingredients to IngredientList\n
    Clears UserIngredients list
    :param request:
    :param action:
    :return:
    """
    if action == 'add':
        serializer = ingredientListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if action == 'clear':
        userIngredients.objects.all().delete()
        return Response("Success")
