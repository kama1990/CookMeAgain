# Generated by Django 4.2.3 on 2023-08-02 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookMe', '0003_rename_maincomponets_recipe_maincomponents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='picRecipe',
            field=models.ImageField(blank=True, upload_to='recipePics', verbose_name='Zdjęcie przepisu'),
        ),
    ]