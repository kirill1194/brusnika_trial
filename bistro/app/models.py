from django.db import models


class Allergen(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название')

    def __str__(self):
        return f"{self.name}"


class Dish(models.Model):
    # Категории
    CATEGORY_CHOICES = (
        (None, 'Без категории'),
        (0, 'Закуски'),
        (1, 'Горячие блюда'),
        (2, 'Десерты'),
        (3, 'Напитки'),
        (4, 'Алкогольные напитки')
    )

    name = models.CharField(max_length=100, verbose_name='Название')
    calorie = models.PositiveSmallIntegerField(verbose_name='Калорийность')
    allergen = models.ManyToManyField(Allergen, related_name='dish', verbose_name='Аллергены', blank=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, null=True, blank=True)
    price = models.PositiveSmallIntegerField(verbose_name='Цена')
    picture = models.ImageField(upload_to='static/images/menu/', default='static/images/menu/no_img.jpg')

    def __str__(self):
        return f"{self.name} - {self.price}$"
