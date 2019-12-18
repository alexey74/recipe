from django.contrib import admin

from .models import Recipe, Step, Ingredient

admin.site.register([Recipe, Step, Ingredient])
