# Generated by Django 2.2.7 on 2019-12-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20191211_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.CharField(max_length=200, verbose_name='Автор'),
        ),
    ]
