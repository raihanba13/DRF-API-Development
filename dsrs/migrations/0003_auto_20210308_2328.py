# Generated by Django 3.1 on 2021-03-08 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsrs', '0002_auto_20210308_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='dsrs',
            field=models.CharField(default='', max_length=50),
        ),
    ]