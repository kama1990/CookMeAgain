from django.urls import path
from . import views

app_name = 'rememberMe'

urlpatterns = [
    path('add/<int:post_id>/', views.rememberMe_add, name='rememberMe_add'),
    path('remove/<int:post_id>/', views.rememberMe_remove, name='rememberMe_remove'),
    path('', views.rememberMe_detail, name='rememberMe_detail'), 
]