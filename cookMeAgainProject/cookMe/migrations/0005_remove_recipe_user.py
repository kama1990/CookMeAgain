# Generated by Django 4.2.3 on 2023-09-05 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookMe', '0004_alter_recipe_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='user',
        ),
    ]
