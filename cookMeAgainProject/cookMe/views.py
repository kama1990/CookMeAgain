from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.
def home(request):
    return render(request, 'home.html')

def post_recipe(request):
    postRecipes = Recipe.objects.all().order_by('-create_date') # objects - fetches all objects from the database
    return render(request,
                  'post/postRecipe.html',
                  {'postRecipes':postRecipes})

def post_detail(request, id):
    post = get_object_or_404(Recipe,
                             id=id)
    return render(request,
                  'post/post_detail.html',
                  {'post':post})

def upload(request):
    if request.method == "POST":
        pic_recipes = request.FILES.getlist('pic_recipe')
        for pic_recipe in pic_recipes:
            Recipe.objects.create(pic_recipes=pic_recipe)
    pic_recipes = Recipe.objects.all()
    return render(request, 'postRecipe.html', {'pic_recipes': pic_recipe})