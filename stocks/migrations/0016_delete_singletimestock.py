# Generated by Django 3.2 on 2023-04-04 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0015_singletimestock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SingleTimeStock',
        ),
    ]