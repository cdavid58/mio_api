# Generated by Django 3.2.8 on 2023-02-07 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_inventory_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='quanty',
            field=models.FloatField(),
        ),
    ]
