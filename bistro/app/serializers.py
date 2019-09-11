# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from app.models import *
from rest_framework import serializers


class CreatableAllergenRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name',
                  'calorie',
                  'allergen',
                  'category',
                  'price',
                  'picture')

    name = serializers.CharField(required=True)
    calorie = serializers.IntegerField(required=False)
    allergen = CreatableAllergenRelatedField(many=True,
                                             slug_field='name',
                                             queryset=Allergen.objects.all(),
                                             required=False)
    category = serializers.IntegerField(required=False, allow_null=True)
    price = serializers.IntegerField(required=False)
    picture = serializers.ImageField(required=False)

    def create(self, validated_data):
        allergen_data = validated_data.pop('allergen')
        dish = Dish(**validated_data)
        dish.save()

        # Добавляем m2m связи к аллергенам
        for allergen_item in allergen_data:
            allergen = Allergen.objects.get(name=allergen_item)
            dish.allergen.add(allergen)
        return dish

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.calorie = validated_data.get('calorie', instance.calorie)
        instance.allergen = validated_data.get('allergen', instance.allergen)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
