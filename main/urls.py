from django.urls import path, include
from django.contrib import admin
from . import views

app_name = "main"
urlpatterns = [
    path('recipesearchdata', views.recipeSearchData, name='recipeSearchData'),
    path('recipemultipledata', views.recipeMultipleData, name='recipeMultipleData'),
    path('recipesingledata', views.recipeSingleData, name='recipeSingleData'),
    path('savedrecipedata', views.savedRecipeData, name='savedRecipeData'),
]
