'''
Recipe app models
'''


from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Recipe(models.Model):
    '''
    Recipe model.
    '''
    name = models.CharField(_('Name'), max_length=255, help_text=_('Recipe name'))
    user = models.ForeignKey(User, related_name='recipes', help_text=_('Recipe owner'), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Step(models.Model):
    '''
    Recipe step model.
    '''
    recipe = models.ForeignKey('core.Recipe', related_name='steps', on_delete=models.CASCADE,
                               help_text=_('Recipe this step is a part of'))
    step_text = models.CharField(_('Step Description'), max_length=255, help_text=_('Step description'))

    def __str__(self):
        return self.step_text


class Ingredient(models.Model):
    '''
    Recipe ingredient model.
    '''
    recipe = models.ForeignKey('core.Recipe', related_name='ingredients', on_delete=models.CASCADE,
                               help_text=_('Recipe this ingredient is a part of'))
    text = models.CharField(_('Ingredient Description'), max_length=255,
                            help_text=_('Ingredient description'))

    def __str__(self):
        return self.text
