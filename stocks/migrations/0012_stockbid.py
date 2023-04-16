# Generated by Django 3.2 on 2023-03-28 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0011_auto_20230326_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockBid',
            fields=[
                ('stockBidId', models.AutoField(primary_key=True, serialize=False)),
                ('boughtCount1', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('boughtCount2', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('boughtCount3', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('boughtCount4', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('boughtCount5', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('boughtPrice1', models.FloatField(blank=True, null=True, verbose_name='')),
                ('boughtPrice2', models.FloatField(blank=True, null=True, verbose_name='')),
                ('boughtPrice3', models.FloatField(blank=True, null=True, verbose_name='')),
                ('boughtPrice4', models.FloatField(blank=True, null=True, verbose_name='')),
                ('boughtPrice5', models.FloatField(blank=True, null=True, verbose_name='')),
                ('date', models.CharField(blank=True, max_length=255, null=True, verbose_name='')),
                ('sellCount1', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('sellCount2', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('sellCount3', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('sellCount4', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('sellCount5', models.IntegerField(blank=True, null=True, verbose_name='')),
                ('sellPrice1', models.FloatField(blank=True, null=True, verbose_name='')),
                ('sellPrice2', models.FloatField(blank=True, null=True, verbose_name='')),
                ('sellPrice3', models.FloatField(blank=True, null=True, verbose_name='')),
                ('sellPrice4', models.FloatField(blank=True, null=True, verbose_name='')),
                ('sellPrice5', models.FloatField(blank=True, null=True, verbose_name='')),
                ('stockNum', models.CharField(blank=True, max_length=255, null=True, verbose_name='')),
                ('time', models.CharField(blank=True, max_length=255, null=True, verbose_name='')),
            ],
        ),
    ]