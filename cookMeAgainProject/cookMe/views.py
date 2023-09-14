from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Recipe, Category
from .forms import EmailPostForm, RecipePostForm, CategoryForm
from rememberMe.forms import RememberMeAddRecipeForm
from cookMeAgain.settings import EMAIL_HOST_USER

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def post_recipe(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    post_recipe = Recipe.objects.all().order_by('-create_date') # objects - fetches all objects from the database
    amount_of_all_recipes = Recipe.objects.all().count()
    
    paginator = Paginator(post_recipe,6) # 6 recipes on 1 page
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
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        post_recipe = post_recipe.filter(category=category)
    return render(request,
                  'post/postRecipe.html',
                  {'posts':posts,
                   'category':category,
                   'categories':categories,
                   'post_recipe':post_recipe,
                   'amount_of_all_recipes':amount_of_all_recipes})


def post_detail(request, id, slug):
    post = get_object_or_404(Recipe,
                             id=id,
                             slug=slug)
    rememberMe_recipe_form = RememberMeAddRecipeForm()
    return render(request,
                  'post/post_detail.html',
                  {'post':post,
                   'rememberMe_recipe_form':rememberMe_recipe_form})

@login_required
def post_share(request, post_id):
    post = get_object_or_404(Recipe, id=post_id)
    sent = False
    if request.method == 'POST':
        # the form was sent
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form is valid
            cd = form.cleaned_data # if something went wrong, cd will contain only correct info'
            # .. sent email
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"Użytkownik {cd['name']} udostępnił Ci przepis {post.title}"
            message = f"Sprawdź {post.title} pod adresem {post_url}\n\n" \
                      f"Wiadomość od użytkownika {cd['name']}: {cd['comments']}"
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()   
    return render(request,
                  'post/share.html',
                  {'post':post,
                   'form':form,
                   'sent':sent})

@login_required
def create_new_recipe(request):
    if request.method == 'GET': # When used GET method eg. web loading, create empty creation form
        return render(request,
                      'post/create_new_recipe.html',
                      {'form':RecipePostForm()})
    else:
        form = RecipePostForm(request.POST, request.FILES)
        # create RecipePostForm and fill it with request data, request.FILES are neccesery for image which user would like to upload
        if form.is_valid(): # if data is valid
            post = form.save(commit=False) # create post but it will be not save yet
            post.user = request.user # we have to add user
            post.save() # no, we can save
            return redirect('post_recipe')
        else: # if something went wrong
            error = "Coś poszło nie tak"
            return render(request,
                          'post/create_new_recipe.html',
                          {'form': RecipePostForm(),
                           'error':error})

@login_required        
def delete_recipe(request, post_id):
    post = get_object_or_404(Recipe,
                             id=post_id)
                            #  user=request.user)
    post.delete()
    return render(request,
                  'post/delete.html')

@login_required
def edit_recipe(request, post_id):
    # Use get() to return an object, or raise a Http404 exception if the object does not exist.
    post = get_object_or_404(Recipe,
                            id=post_id)
                            # user=request.user)
    if request.method == 'GET':
        form = RecipePostForm(instance=post)
        return render(request,
                      'post/edit_recipe.html',
                      {'form':form,
                       'post':post})
    else:
        # we want to fillin RecipePostForm for exist post , user is there  /  user jest zaciagny z instancji/
        form = RecipePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_recipe')
        else:
            error = "Coś poszło nie tak, spróbuj raz jeszcze"
            return render(request,
                          'post/edit_recipe.html',
                          {'post':post,
                           'form':form,
                           'error':error})

@login_required
def create_new_category(request):
    if request.method == 'GET':
        return render(request,
                      'post/create_new_category.html', {'form':CategoryForm()})
    else:
        form = CategoryForm(request.POST, request.FILES)
        name = request.POST.get('name')
        slug = name.replace(" ","-")
        if form.is_valid():
            slugTaken = Category.objects.filter(slug=slug).exists()
            if slugTaken:
                error = "Podana kategoria już istnieje"
            else:
                new_category = form.save(commit=False)
                new_category.user = request.user
                new_category.save()
                return redirect('post_recipe')
        else:
            error = "Coś poszło nie tak"
        return render(request,
                      'post/create_new_category.html',
                      {'form':CategoryForm(),
                       'error':error})

@login_required    
def delete_category(request, category_id):
    category = get_object_or_404(Category,
                                 id=category_id)
    category.delete()
    #   later add possiblity to ask one more time - are you sure to delete category
    return redirect('post_recipe') 

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category,
                                 id=category_id)
    if request.method == "GET":
        form = CategoryForm(instance=category)
        return render(request,
                      'post/edit_category.html',
                      {'form':form,
                       'category':category})
    else:
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('post_recipe')
        else:
            error = "Coś poszło nie tak"
            return render(request,
                          'post/edit_category.html',
                          {'category':category,
                           'form':form,
                           'error':error})

def upload(request):
    if request.method == "POST":
        pic_recipes = request.FILES.getlist('pic_recipe')
        for pic_recipe in pic_recipes:
            Recipe.objects.create(pic_recipes=pic_recipe)
    pic_recipes = Recipe.objects.all()
    return render(request, 'postRecipe.html', {'pic_recipes': pic_recipe})