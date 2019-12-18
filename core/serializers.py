'''

Recipe app serializers

'''

from rest_framework import serializers

from .models import Recipe, Step, Ingredient


class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = '__all__'


class StepSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = Step
        exclude = ('recipe',)

    id = serializers.IntegerField(required=False)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ('recipe',)

    id = serializers.IntegerField(required=False)


class RecipeSerializer(serializers.ModelSerializer):
    steps = StepSerializerNested(many=True, required=False)
    ingredients = IngredientSerializerNested(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'user', 'steps', 'ingredients')

    def create(self, validated_data):
        '''
        Create Recipe instance.

        Creates main instance first, then related instances
        (steps and ingredients) if specified in `validated_data`.

        :param validated_data: data to create instance with
        :type validated_data: dict
        :returns: created instance
        :rtype: instance of Recipe
        '''
        steps_data = validated_data.pop('steps', [])
        ingredients_data = validated_data.pop('ingredients', [])

        recipe = Recipe.objects.create(**validated_data)

        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        '''
        Update Recipe instance.

        Updates local fields on the instance, then searches
        related instances (steps and ingredients) by their IDs
        given in the `validated_data` substructures,
        then updates their field accordingly.

        :param instance: Recipe instance to update
        :param validated_data: data to update instance with
        :returns: updated instance
        '''
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        steps = validated_data.get('steps', [])
        for step_data in steps:
            step = instance.steps.get(pk=step_data['id'])
            step.step_text = step_data['step_text']
            step.save()

        ingredients = validated_data.get('ingredients', [])
        for ingr_data in ingredients:
            ingr = instance.steps.get(pk=ingr_data['id'])
            ingr.text = ingr_data['text']
            ingr.save()

        return instance
