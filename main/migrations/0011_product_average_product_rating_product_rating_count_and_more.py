# Generated by Django 4.0.5 on 2022-06-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_review_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='average',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='rating_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1),
        ),
    ]
