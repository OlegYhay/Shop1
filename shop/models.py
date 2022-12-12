import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['title']

    STATUS = (
        ('В наличии', 'В наличии'),
        ('Под заказ', 'Под заказ'),
        ('Ожидается поступление', 'Ожидается поступление'),
        ('Нет в наличии', 'Нет в начилии'),
        ('Не производится', 'Не производится'),
    )
    # Required fields from the task
    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=255)
    category = models.ForeignKey(verbose_name=_('category'), to='Category', on_delete=models.PROTECT,
                                 related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price', default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, default='В наличии')

    # ---
    def __str__(self):
        return self.title

    # сохраняется оба варианта(в заданий не уточнялось), но используется webq.
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if '.jpg' in self.image.url or '.png' in self.image.url:
            img_io = BytesIO()
            im = Image.open(self.image).convert('RGB')
            im.save(img_io, format='WEBP')
            name = os.path.splitext(os.path.basename(self.image.name))[0] + '.webp'
            self.image = ContentFile(img_io.getvalue(), name)
            super(Product, self).save(*args, **kwargs)


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)

    property_objects = models.ManyToManyField(verbose_name=_('properties'), to='PropertyObject')

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(_('value type'), max_length=10, choices=Type.choices)

    def __str__(self):
        return f'{self.title} ({self.get_value_type_display()})'


class PropertyValue(models.Model):
    class Meta:
        verbose_name = _('property value')
        verbose_name_plural = _('properties values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(to=PropertyObject, on_delete=models.PROTECT)

    value_string = models.CharField(_('value string'), max_length=255, blank=True, null=True)
    value_decimal = models.DecimalField(_('value decimal'), max_digits=11, decimal_places=2, blank=True, null=True)
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product, related_name='properties')

    def __str__(self):
        return str(getattr(self, f'value_{self.property_object.value_type}', None))
