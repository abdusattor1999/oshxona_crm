# Generated by Django 4.0 on 2023-07-27 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_alter_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Chiqim nomi')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Batafsil')),
                ('is_product', models.BooleanField(default=False, verbose_name='Maxsulot olindimi')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Chiqim umumiy summasi')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Chiqim vaqti')),
                ('kitchen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.kitchen', verbose_name='Oshxona')),
            ],
        ),
        migrations.CreateModel(
            name='OutputItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=50, verbose_name='Maxsulot nomi')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Batafsil')),
                ('amount', models.CharField(blank=True, max_length=25, null=True, verbose_name='Miqdori')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Narxi')),
                ('output', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='outputs.output')),
            ],
        ),
    ]
