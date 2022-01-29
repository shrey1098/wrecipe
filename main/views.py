from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .serializers import recipeSerializerPost, userIngredientsSerializer
from .services import getRecipesData, getRecipeData, postRecipeData, getSearchRecipe, getUserRecipes, likeOrUnlike, \
    getSavedRecipes, saveOrUnsave, postDeleteRecipe, getIngredient, getSearchIngredient, postAddNewUserIngredients,\
    getActionUserIngredients, postActionUserIngredients


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipesData(request):
    """
    *api url: /api.recipesdata* \n
    :param request:
    :return: json serialized list of all recipes
    """
    return getRecipesData(request)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recipeData(request):
    """
    *api url: /api.recipedata* \n
    :param request:
    :return:
    """
    if request.method == 'GET':
        return getRecipeData(recipeID=request.GET['id'], user=request.user)

    if request.method == 'POST':
        return postRecipeData(serializer=recipeSerializerPost(data=request.data), user=request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipeSearch(request):
    """
    *api url: /api.recipesearch* GET Method only,
    :param request:
    :return:
    """
    return getSearchRecipe(query=request.GET['q'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userRecipesData(request):
    """
    *api url: api.userrecipesdata *\n
    :param request:
    :return:
    """
    return getUserRecipes(user=request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def likeRecipe(request):
    """
    *api url:/api.likerecipe?id= * \n
    :param request:
    :return:Liked or unliked
    """
    return likeOrUnlike(recipeID=request.GET['id'], user=request.user)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def savedRecipesData(request):
    """
    *api url: /api.savedrecipesdata?id=*\n
    :param request:
    :return:
    """
    if request.method == 'GET':
        return getSavedRecipes(user=request.user.id)

    if request.method == 'POST':
        return saveOrUnsave(recipeID=request.GET['id'], user=request.userr)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteRecipe(request):
    """
    *api url: api.deleterecipe?id=*\n
    :param request:
    :return:
    """
    return postDeleteRecipe(recipeID=request.GET['id'], user=request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ingredientSearch(request):
    """
    *api url:/api.ingredientsearch?q=*\n
    :param request:
    :return:JSON list of all matching queries
    """
    return getSearchIngredient(query=request.GET['q'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getIngredient(request):
    """
    *api url: api.getingredients?id=*\n
    :param request:
    :return:
    """
    return getIngredient(ingredientID=request.GET['id'])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addUserIngredients(request):
    """
    *api url: /api.adduseringredient *\n
    Adds new ingredients which does not exist in ingredientList model to the user ingredient model.
    :param request:
    :return:
    """
    return postAddNewUserIngredients(serializer=userIngredientsSerializer(data=request.data))


@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def actionUserIngredients(request):
    """
    *api url: api.useringredientsaction*\n
    :param request:
    :return:
    """
    if request.method == 'GET':
        return getActionUserIngredients()
    if request.method == 'POST':
        action = request.GET['action']
        postActionUserIngredients(request, action)

def googleAuthObtainToken(request):
    user = request.user.id
    token =Token.objects.get_or_create(user_id=user)
    return token
