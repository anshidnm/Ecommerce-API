# Generated by Django 4.0.5 on 2022-06-23 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_product_order_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(default='./static/img/team_4.jpg', upload_to='brands'),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='./static/img/team_4.jpg', upload_to='categories'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='./static/img/team_4.jpg', upload_to='products'),
        ),
    ]