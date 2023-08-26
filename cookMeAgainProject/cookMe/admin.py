from django.contrib import admin
from .models import Recipe

# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'my_rating', 'create_date', 'user' ]
    list_filter = ['my_rating', 'create_date']
    search_fields = ['title', 'main_components']
