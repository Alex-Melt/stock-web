# Generated by Django 3.2 on 2023-03-16 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_alter_sys_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sys_user',
            name='mobile',
            field=models.IntegerField(blank=True, verbose_name='手机号码'),
        ),
    ]
