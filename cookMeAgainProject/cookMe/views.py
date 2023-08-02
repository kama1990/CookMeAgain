from django.shortcuts import render
from .models import Recipe

# Create your views here.
def home(request):
    return render(request, 'home.html')

def postRecipe(request):
    postRecipes = Recipe.objects.all().order_by('-createDate') # objects - fetches all objects from the database
    return render(request, 'postRecipe.html', {'post':postRecipes})