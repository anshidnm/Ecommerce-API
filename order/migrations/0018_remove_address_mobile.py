# Generated by Django 3.2.13 on 2022-06-28 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_alter_address_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='mobile',
        ),
    ]
