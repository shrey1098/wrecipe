# Generated by Django 3.2.4 on 2021-06-22 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('visibilityType', models.CharField(choices=[('PR', 'Private'), ('PU', 'Public')], default='Public', max_length=20)),
                ('recipeType', models.CharField(choices=[('V', 'Veg'), ('NV', 'Non-Veg'), ('VE', 'Vegan')], max_length=20)),
                ('mealType', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner'), ('S', 'Snack'), ('DE', 'Dessert')], max_length=20)),
                ('servingSize', models.PositiveIntegerField(default=None)),
                ('cookingTime', models.PositiveIntegerField(default=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
