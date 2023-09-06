from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.post_recipe, name='post_recipe'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('createNewRecipe/', views.create_new_recipe, name='create_new_recipe'),
    path('<int:post_id>/deleteRecipe/', views.delete_recipe, name='delete_recipe'),
    path('<int:category_id>/deleteCategory/', views.delete_category, name='delete_category'),
    path('<int:post_id>/editRecipe/', views.edit_recipe, name='edit_recipe'),
    path('<int:category_id>/editCategory/', views.edit_category, name='edit_category'),
    path('createNewCategory/', views.create_new_category, name='create_new_category'),
    path('<slug:category_slug>/', views.post_recipe, name='post_recipe_by_category'),
    path('<int:id>/<slug:slug>/', views.post_detail, name='post_detail'),
    
]
