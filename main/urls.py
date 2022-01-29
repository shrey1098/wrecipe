from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = "main"
urlpatterns = [
    path('api.recipesearch', views.recipeSearch, name='recipeSearch'),
    path('api.recipesdata', views.recipesData, name='recipesData'),
    path('api.recipedata', views.recipeData, name='recipeData'),
    path('api.savedrecipesdata', views.savedRecipesData, name='savedRecipesData'),
    path('api.likerecipe', views.likeRecipe, name='likeRecipe'),
    path('api.userrecipesdata', views.userRecipesData, name='userRecipesData'),
    path('api.deleterecipe', views.deleteRecipe, name='deleteRecipe'),
    path('api.ingredientsearch', views.ingredientSearch, name='ingredientSearch'),
    path('api.getingredient', views.getIngredient, name='getIngredient'),
    path('api.adduseringredient', views.addUserIngredients, name='adduserIngredients'),
    path('api.useringredientsaction', views.actionUserIngredients, name='actionUserIngredients'),
    path('api.apitoken', obtain_auth_token, name='obtainToken'),
    path('api.rest-auth/', include('rest_auth.urls')),
    path('api.rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api.gettoken', views.googleAuthObtainToken,name='googleAuthenticationObtainToken'),
]
