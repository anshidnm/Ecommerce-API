# Generated by Django 4.0.5 on 2022-06-17 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_product_is_added_to_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Is_added_to_cart',
        ),
    ]
