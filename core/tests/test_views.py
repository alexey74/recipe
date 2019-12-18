from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Recipe, Step, Ingredient

from .factories import RecipeFactory, StepFactory, IngredientFactory


class RecipeViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'testpasswd')

    def test_simple_create_recipe_returns_original_data(self):
        data = {'name': 'Test recipe', 'user': self.user.pk}

        response = self.client.post(reverse('recipe-list'), data=data)

        self.assertEqual(Recipe.objects.count(), 1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['user'], data['user'])

    def test_nested_create_recipe_returns_original_data(self):
        data = {'name': 'Test recipe', 'user': self.user.pk,
                'steps': [{'step_text': 'Test step text 1'}, {'step_text': 'Test step text 2'}],
                'ingredients': [{'text': 'Test ingredient 1'},
                                {'text': 'Test ingredient 2'},
                                {'text': 'Test ingredient 3'},
                                ],

                }

        response = self.client.post(reverse('recipe-list'), data=data)

        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Step.objects.count(), 2)
        self.assertEqual(Ingredient.objects.count(), 3)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['user'], data['user'])

    def test_filter_by_user_id_returns_matching_recipes_only(self):
        recipe = RecipeFactory(name='test recipe', user=self.user)
        user1 = User.objects.create_user('testuser1', 'testuser1@example.com', 'testpasswd')
        recipe1 = RecipeFactory(name='test recipe 1', user=user1)

        response = self.client.get(reverse('recipe-list'),
                                   data={'user': self.user.pk}
                                   )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data['results']), 1, response.data)
        self.assertEqual(response.data['count'], 1, response.data)
        self.assertEqual(response.data['results'][0]['name'], 'test recipe', response.data)

    def test_search_by_user_name_returns_matching_recipes_only(self):
        recipe = RecipeFactory(name='test recipe', user=self.user)
        user1 = User.objects.create_user('testuser1', 'testuser1@example.com', 'testpasswd')
        recipe1 = RecipeFactory(name='test recipe 1', user=user1)

        response = self.client.get(reverse('recipe-list'),
                                   data={'search': 'testuser1'}
                                   )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data['results']), 1, response.data)
        self.assertEqual(response.data['count'], 1, response.data)
        self.assertEqual(response.data['results'][0]['name'], 'test recipe 1', response.data)

    def test_bare_list_returns_all_recipes(self):
        for _ in range(5):
            recipe = RecipeFactory()
            for __ in range(3):
                StepFactory(recipe=recipe)
            for __ in range(5):
                IngredientFactory(recipe=recipe)

        response = self.client.get(reverse('recipe-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data['results']), 5, response.data)
        for recipe in response.data['results']:
            self.assertEqual(len(recipe['steps']), 3, response.data)
            self.assertEqual(recipe['steps'][0]['id'],
                             Recipe.objects.get(pk=recipe['id']).steps.first().pk,
                             response.data)
            self.assertEqual(len(recipe['ingredients']), 5, response.data)

    def test_update_recipe_name_only(self):
        recipe = RecipeFactory()
        for __ in range(3):
            StepFactory(recipe=recipe)
        for __ in range(5):
            IngredientFactory(recipe=recipe)

        response = self.client.patch(reverse('recipe-detail', args=(recipe.pk,)),
                                     data={'name': 'new name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['name'], 'new name', response.data)
        self.assertEqual(Recipe.objects.get(pk=recipe.pk).name, 'new name')

        self.assertEqual(len(response.data['steps']), 3, response.data)
        self.assertEqual(len(response.data['ingredients']), 5, response.data)

    def test_update_steps_only(self):
        recipe = RecipeFactory(name='test recipe')
        for i in range(3):
            StepFactory(recipe=recipe, step_text=f'step {i}')
        for j in range(5):
            IngredientFactory(recipe=recipe, text=f'ingr. {j}')

        response = self.client.patch(
            reverse('recipe-detail', args=(recipe.pk,)),
            data={
                'steps': [
                    {
                        'id': recipe.steps.first().pk,
                        'step_text': 'new text',
                    }
                ]})

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data['steps']), 3, response.data)
        self.assertEqual(len(response.data['ingredients']), 5, response.data)

        self.assertEqual(response.data['steps'][0]['step_text'], 'new text', response.data)
        self.assertEqual(response.data['steps'][1]['step_text'], 'step 1', response.data)

    def test_delete_recipe(self):
        recipe = RecipeFactory(name='test recipe')
        for i in range(3):
            StepFactory(recipe=recipe, step_text=f'step {i}')
        for j in range(5):
            IngredientFactory(recipe=recipe, text=f'ingr. {j}')

        response = self.client.delete(
            reverse('recipe-detail', args=(recipe.pk,)),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertEqual(Step.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)
