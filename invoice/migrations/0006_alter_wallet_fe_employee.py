# Generated by Django 3.2.8 on 2022-12-15 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_remove_employee_count_intent_block'),
        ('invoice', '0005_wallet_fe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet_fe',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
    ]