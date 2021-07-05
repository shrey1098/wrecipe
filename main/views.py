# from django.shortcuts import render
# from django.contrib.auth.models import User
from django.db.models import F

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import recipeMultipleSerializer, recipeSerializer, savedRecipeSerializer, ingredientListSerializer, \
    userIngredientsSerializer
from .models import recipe, savedRecipe, ingredientsList, userIngredients


@api_view(['GET'])
@permission_classes([AllowAny])
def recipeMultipleData(request):
    if not request.GET:
        # ToDo: get 15 objects at once, later when user has scrolled through them all call again and return next 15
        qs = recipe.objects.all()
        q = list(reversed(qs))
        serializer = recipeMultipleSerializer(q, many=True)
        return Response(serializer.data)
    else:
        qs = recipe.objects.filter(name__contains=request.GET['query'])
        serializer = recipeMultipleSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recipeSingleData(request):
    if request.method == 'GET':
        recipeID = request.GET['id']
        qs = recipe.objects.get(pk=recipeID)
        recipe.objects.filter(pk=recipeID).update(views=F('views') + 1)
        print(request.user)
        serializer = recipeSerializer(qs)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = recipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['name'] = serializer.validated_data['name'].capitalize()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userRecipeData(request):
    user = request.user
    qs = recipe.objects.filter(user=user)
    serializer = recipeMultipleSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def savedRecipeData(request):
    if request.method == 'GET':
        user = request.user.id
        qs = savedRecipe.objects.filter(user=user)
        serializer = savedRecipeSerializer(qs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = savedRecipeSerializer(data=request.data)
        recipeID = request.data['name']
        recipe.objects.filter(pk=recipeID).update(saves=F('saves') + 1)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteRecipe(request):
    recipeID = request.GET['id']
    user = recipe.objects.filter(pk=recipeID).get().user
    if user == request.user:
        recipe.objects.filter(pk=recipeID).delete()
        return Response({'Deleted Successfully'})
    else:
        return Response({'Can not delete other user recipes'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getIngredients(request):
    ingredientID = request.GET['id']
    qs = ingredientsList.objects.get(pk=ingredientID)
    serializer = ingredientListSerializer(qs)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def addNewIngredients(request):
    serializer = ingredientListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def actionUserIngredients(request):
    if request.method =='GET':
        qs = userIngredients.objects.all()
        serializer = userIngredientsSerializer(qs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        q = request.GET['action']
        if q == 'add':
            serializer = userIngredientsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        if q == 'clear':
            userIngredients.objects.all().delete()
            return Response("Success")