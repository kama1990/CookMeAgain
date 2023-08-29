from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Recipe

# Create your views here.
def home(request):
    return render(request, 'home.html')

def post_recipe(request):
    post_recipe = Recipe.objects.all().order_by('-create_date') # objects - fetches all objects from the database
    paginator = Paginator(post_recipe,3) # 5 recipes on 1 page
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not integer
        # shows first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number will not exist
        # shows last page
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'post/postRecipe.html',
                  {'posts':posts})

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