# Generated by Django 3.2.13 on 2022-06-28 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
        ('main', '0026_stock_manage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='master_product',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='master.masterproduct'),
        ),
    ]
