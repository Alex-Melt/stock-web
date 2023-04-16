# Generated by Django 3.2 on 2023-04-04 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0014_rename_sourceform_news_sourcefrom'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleTimeStock',
            fields=[
                ('timeInfoId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('stockId', models.IntegerField(blank=True, null=True)),
                ('stockCode', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('avgPrice', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('volume', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True)),
                ('upDownRange', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
            ],
        ),
    ]
