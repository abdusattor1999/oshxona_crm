# Generated by Django 4.0 on 2023-07-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outputs', '0002_rename_name_output_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='Chiqim umumiy summasi'),
        ),
        migrations.AlterField(
            model_name='outputitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Narxi'),
        ),
    ]
