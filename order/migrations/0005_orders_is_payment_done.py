# Generated by Django 4.0.5 on 2022-06-17 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_payment_amount_alter_payment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='is_payment_done',
            field=models.BooleanField(default=False),
        ),
    ]
