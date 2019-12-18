from django.contrib.auth.models import User
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')


class StepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Step'

    step_text = factory.Faker('sentence')


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Ingredient'

    text = factory.Faker('sentence')


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Recipe'

    name = factory.Faker('name')
    user = factory.SubFactory(UserFactory)
