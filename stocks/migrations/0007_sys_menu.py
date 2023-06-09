# Generated by Django 3.2 on 2023-03-20 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_auto_20230317_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sys_menu',
            fields=[
                ('menu_id', models.IntegerField(primary_key=True, serialize=False)),
                ('parent_id', models.IntegerField(blank=True, null=True, verbose_name='父菜单ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='菜单名称')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='菜单URL')),
                ('perms', models.CharField(blank=True, max_length=200, null=True, verbose_name='授权(多个用逗号隔开，如：user:list)')),
                ('type', models.IntegerField(blank=True, null=True, verbose_name='类型 0:目录 1:菜单 ')),
                ('icon', models.CharField(blank=True, max_length=30, null=True, verbose_name='菜单图标')),
                ('order_num', models.IntegerField(blank=True, null=True, verbose_name='排序 ')),
            ],
        ),
    ]
