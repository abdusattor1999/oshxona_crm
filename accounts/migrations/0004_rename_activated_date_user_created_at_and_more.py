# Generated by Django 4.0 on 2023-07-08 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_worker_created_alter_kitchen_slug_alter_worker_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='activated_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_seller',
        ),
    ]
