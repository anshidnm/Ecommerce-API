# Generated by Django 4.0.5 on 2022-06-15 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_review'),
    ]

    operations = [
        migrations.DeleteModel(
            name='test',
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
