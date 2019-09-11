# -*- coding: utf-8 -*-
import os
from .models import *
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.six import BytesIO

required_params = {"calorie": 1024,
                   "category": 3,
                   "price": 180,
                   "name": "Милкшейк",
                   "token": "93138ba960dfb4ef2eef6b907718ae04400f606a"}


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class AddDishTests(TestCase):
    def test_required_params(self):
        self.assertEquals(Dish.objects.count(), 0)
        response = self.client.post('/api/add_dash', required_params, follow=True)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(Dish.objects.count(), 1, 'New dish record not created')
        self.assertEquals(Dish.objects.first().picture,
                          'static/images/menu/no_img.jpg',
                          'New dish picture have strange value')

    def test_required_params_plus_allergen(self):
        self.assertEquals(Dish.objects.count(), 0)
        required_params.update({'allergen': ['Арахис']})
        response = self.client.post('/api/add_dash', required_params, follow=True)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(Dish.objects.count(), 1, 'New dish record not created')
        self.assertEquals(Dish.objects.first().picture,
                          'static/images/menu/no_img.jpg',
                          'New dish picture have strange value')
        self.assertTrue(Allergen.objects.filter(name='Арахис'), 'New dish allergen record not created')


class AddDishWithPictureTests(TestCase):
    default_images_folder = 'static/images/menu/test_pic.png'

    def test_required_params_plus_pic(self):
        self.assertEquals(Dish.objects.count(), 0)

        pic = create_image(None, 'pic.png')
        pic_file = SimpleUploadedFile('test_pic.png', pic.getvalue())
        required_params.update({'picture': pic_file})
        response = self.client.post('/api/add_dash', required_params, follow=True)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(Dish.objects.count(), 1, 'New dish record not created')
        self.assertEquals(Dish.objects.first().picture,
                          self.default_images_folder,
                          'New dish picture not created')

    def tearDown(self):
        # Удаляем созданное выше изображение
        os.remove(self.default_images_folder)
