from django.contrib import admin
from app.models import *


class AllergenAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DishAdmin(admin.ModelAdmin):
    filter_horizontal = ('allergen',)
    list_display = ('name',
                    'calorie',
                    'category',
                    'price',
                    'picture')


admin.site.register(Dish, DishAdmin)
admin.site.register(Allergen, AllergenAdmin)
