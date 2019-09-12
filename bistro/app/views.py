from django.shortcuts import render
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.models import Dish, Allergen
from app.serializers import DishSerializer


def get_menu(request):
    menu = Dish.objects.all().order_by('category')
    category = Dish.CATEGORY_CHOICES

    return render(request, 'menu.html', {"menu": menu, "category": category})


@api_view(['POST'])
def subtotal(request):
    dish_ids = dict(request.data).get('dish', [])
    dish_items = Dish.objects.filter(id__in=dish_ids)

    summ = []
    dish_list = []
    allergen_list = []

    for dish in dish_items:
        summ.append(dish.price)
        dish_list.append(dish.name)
        if dish.allergen.exclude():
            [allergen_list.append(allergen.name) for allergen in dish.allergen.all()]

    return render(request, 'subtotal.html', {'summ': sum(summ),
                                             'dish_list': dish_list,
                                             'allergen_list': allergen_list if allergen_list else None})


@api_view(['POST'])
def add_dish(request):
    try:
        if not request.data.get('token') or request.data['token'] != settings.TOKEN:
            raise ValueError('authentication credentials were not provided')

        serializer = DishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(DishSerializer(Dish.objects.all(), many=True).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
