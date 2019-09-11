from django.shortcuts import render
from rest_framework.decorators import api_view
from app.models import Dish, Allergen


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

    if dish_ids:
        for dish in dish_items:
            summ.append(dish.price)
            dish_list.append(dish.name)
            if dish.allergen.exclude():
                [allergen_list.append(allergen.name) for allergen in dish.allergen.all()]

    return render(request, 'subtotal.html', {'summ': sum(summ),
                                             'dish_list': dish_list,
                                             'allergen_list': allergen_list if allergen_list else None})
