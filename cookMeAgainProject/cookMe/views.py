from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Recipe
from .forms import EmailPostForm, RecipePostForm
from cookMeAgain.settings import EMAIL_HOST_USER

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
        
def delete_recipe(request, post_id):
    post = get_object_or_404(Recipe,
                             id=post_id,
                             user=request.user)
    post.delete()
    return render(request,
                  'post/delete.html')

def upload(request):
    if request.method == "POST":
        pic_recipes = request.FILES.getlist('pic_recipe')
        for pic_recipe in pic_recipes:
            Recipe.objects.create(pic_recipes=pic_recipe)
    pic_recipes = Recipe.objects.all()
    return render(request, 'postRecipe.html', {'pic_recipes': pic_recipe})