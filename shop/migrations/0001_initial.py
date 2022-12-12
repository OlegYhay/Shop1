# Generated by Django 4.1.4 on 2022-12-12 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('sku', models.CharField(max_length=255, unique=True, verbose_name='sku')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/product/')),
                ('status', models.CharField(choices=[('В наличии', 'В наличии'), ('Под заказ', 'Под заказ'), ('Ожидается поступление', 'Ожидается поступление'), ('Нет в наличии', 'Нет в начилии'), ('Не производится', 'Не производится')], default='В наличии', max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PropertyObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('code', models.SlugField(max_length=255, verbose_name='code')),
                ('value_type', models.CharField(choices=[('string', 'string'), ('decimal', 'decimal')], max_length=10, verbose_name='value type')),
            ],
            options={
                'verbose_name': 'property object',
                'verbose_name_plural': 'properties objects',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PropertyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_string', models.CharField(blank=True, max_length=255, null=True, verbose_name='value string')),
                ('value_decimal', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='value decimal')),
                ('code', models.SlugField(max_length=255, verbose_name='code')),
                ('products', models.ManyToManyField(related_name='properties', to='shop.product')),
                ('property_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.propertyobject')),
            ],
            options={
                'verbose_name': 'property value',
                'verbose_name_plural': 'properties values',
                'ordering': ['value_string', 'value_decimal'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='property_objects',
            field=models.ManyToManyField(to='shop.propertyobject', verbose_name='properties'),
        ),
    ]