from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cookMe.models import Recipe
from .rememberMe import RememberMe
from .forms import RememberMeAddRecipeForm
# Create your views here.
@require_POST
def rememberMe_add(request, post_id):
    rememberMe = RememberMe(request)
    post = get_object_or_404(Recipe, id=post_id)
    form = RememberMeAddRecipeForm(request.POST)
    if form.is_valid():
        # cd = form.cleaned_data
        rememberMe.add(post=post)
    # return render(request,
    #               'rememberMe/detail.html',
    #               {'rememberMe':rememberMe,
    #                'post':post,
    #                'form':form})
    return redirect('rememberMe:rememberMe_detail')

@require_POST
def rememberMe_remove(request, post_id):
    rememberMe = RememberMe(request)
    post = get_object_or_404(Recipe, id=post_id)
    rememberMe.remove(post)
    return render(request,
                  'rememberMe/detail.html',
                  {'rememberMe':rememberMe,
                   'post':post})
    return redirect('rememberMe:rememberMe_detail')

def rememberMe_detail(request):
    rememberMe = RememberMe(request)
    return render(request,
                  'rememberMe/detail.html',
                  {'rememberMe':rememberMe})
    return redirect('rememberMe:rememberMe_detail')