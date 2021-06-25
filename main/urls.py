from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = "main"
urlpatterns = [
    path('api.recipemultipledata', views.recipeMultipleData, name='recipeMultipleData'),
    path('api.recipesingledata', views.recipeSingleData, name='recipeSingleData'),
    path('api.savedrecipedata', views.savedRecipeData, name='savedRecipeData'),
    path('api.userrecipedata', views.userRecipeData, name='userRecipeData'),
    path('api.deleterecipedata', views.deleteRecipe, name='deleteRecipeData'),
    path('api.apitoken', obtain_auth_token, name='obtainToken'),
    path('api.rest-auth/', include('rest_auth.urls')),
    path('api.rest-auth/registration/', include('rest_auth.registration.urls')),
]
