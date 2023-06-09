# Generated by Django 3.2 on 2023-03-26 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_sys_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stockId', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('amplitude', models.FloatField(blank=True, null=True, verbose_name='振幅')),
                ('close', models.FloatField(blank=True, null=True)),
                ('flowMarketValue', models.FloatField(blank=True, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('listingDate', models.CharField(blank=True, max_length=255, null=True, verbose_name='上市时间')),
                ('low', models.FloatField(blank=True, null=True)),
                ('open', models.FloatField(blank=True, null=True)),
                ('preClose', models.FloatField(blank=True, null=True)),
                ('stockName', models.CharField(blank=True, max_length=255, null=True, verbose_name='股票名称')),
                ('stockNum', models.CharField(blank=True, max_length=255, null=True, verbose_name='股票编号')),
                ('totalFlowShares', models.FloatField(blank=True, null=True, verbose_name='流通股本')),
                ('totalMarketValue', models.FloatField(blank=True, null=True)),
                ('totalShares', models.FloatField(blank=True, null=True)),
                ('turnOverrate', models.FloatField(blank=True, null=True, verbose_name='换手率')),
                ('upDownPrices', models.FloatField(blank=True, null=True, verbose_name='涨跌额')),
                ('upDownRange', models.FloatField(blank=True, null=True, verbose_name='单日涨跌幅')),
                ('upDownRange3', models.FloatField(blank=True, null=True, verbose_name='3日涨跌幅')),
                ('upDownRange5', models.FloatField(blank=True, null=True, verbose_name='5日涨跌幅')),
                ('updateDate', models.CharField(blank=True, max_length=255, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
