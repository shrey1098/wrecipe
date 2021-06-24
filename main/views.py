from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import recipeMultipleSerializer, recipeSerializer, savedRecipeSerializer
from .models import recipe, savedRecipe


@api_view(['GET'])
def recipeMultipleData(request):
    qs = recipe.objects.all()[:5]
    serializer = recipeMultipleSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recipeSearchData(request):
    qs = recipe.objects.filter(name__contains=request.GET['query'])
    serializer = recipeMultipleSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
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


@api_view(['GET', 'POST'])
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
