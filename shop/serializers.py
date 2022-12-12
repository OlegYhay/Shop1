import glob
import os
import pathlib

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from test_shop.settings import MEDIA_ROOT
from .models import *


class SerializerPropertyObject(serializers.ModelSerializer):
    class Meta:
        model = PropertyObject
        fields = ['title']


class SerializerPropertyValue(serializers.ModelSerializer):
    # get info about property object
    property_object = SerializerPropertyObject(read_only=True)

    class Meta:
        model = PropertyValue
        fields = ['property_object', 'value_string', 'value_decimal']


class SerializerCategory(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class SerializerProduct(serializers.ModelSerializer):
    # get info about category and properties
    category = SerializerCategory(read_only=True)
    properties = SerializerPropertyValue(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'sku', 'price', 'image', 'status', 'category', 'properties']

    def to_representation(self, instance):
        response = super(SerializerProduct, self).to_representation(instance)
        if instance.image != None:
            os.chdir(MEDIA_ROOT + '\images' + '\\')
            formats = []
            for file in glob.glob(os.path.splitext(os.path.basename(instance.image.name))[0] + '.*'):
                formats.append(os.path.splitext(file)[1].replace('.',''))
            if instance.image:
                response['image'] = {
                    'path': os.path.splitext(instance.image.url)[0],
                    'formats': formats,
                }
        return response
