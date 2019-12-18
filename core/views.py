'''

Recipe App Views

'''


from django.shortcuts import render
from rest_framework import viewsets

from .models import Recipe, Step, Ingredient
from .serializers import RecipeSerializer, StepSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing recipes.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_fields = ['user']
    search_fields = ['=user__username', '=user__email', ]


class StepViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing recipe steps.
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing recipe ingredients.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
