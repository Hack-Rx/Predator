# Generated by Django 3.0.2 on 2020-06-13 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodNet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='BMI',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.FloatField(null=True),
        ),
    ]
