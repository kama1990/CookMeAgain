from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('postRecipe/', views.post_recipe, name='post_recipe'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]
