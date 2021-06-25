from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import recipeMultipleSerializer, recipeSerializer, savedRecipeSerializer
from .models import recipe, savedRecipe


@api_view(['GET'])
@permission_classes([AllowAny])
def recipeMultipleData(request):
    if not request.GET:
        qs = recipe.objects.all()[:5]
        serializer = recipeMultipleSerializer(qs, many=True)
        return Response(serializer.data)
    else:
        qs = recipe.objects.filter(name__contains=request.GET['query'])
        serializer = recipeMultipleSerializer(qs, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recipeSingleData(request):
    if request.method == 'GET':
        qs = recipe.objects.get(pk=request.GET['id'])
        serializer = recipeSerializer(qs)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = recipeSerializer(data=request.data)
        if serializer.is_valid():
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteRecipe(request):
    recipeID = request.GET['id']
    k = recipe.objects.filter(pk=recipeID).get().user
    if k == request.user:
        recipe.objects.filter(pk=recipeID).delete()
        return Response({'Deleted Successfully'})
    else:
        return Response({'Can not delete other user recipes'})
