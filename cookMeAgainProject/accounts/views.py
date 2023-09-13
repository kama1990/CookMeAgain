from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .form import LoginForm
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) # create form with information
        if form.is_valid(): # is form valid ?
            cd = form.cleaned_data
            # if valid , we authenticate user basted on inforamation in datebase
            # we get username and password and its returns user if user will be authenticate or its returns NONE otherwise
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                # we need to check if account is active
                if user.is_active:
                    login(request, user)
                    return redirect('postRecipe')
            else:
                error = 'Użytkownik nie jest aktywny bądź wprowadzono niepoprawne dane do logowania. Spróbuj ponownie'
                return render(request,
                              'accounts/login.html',
                              {'error':error,
                               'form':form})
        else:
            error = 'Niepoprawne dane do logowania'
            return render(request,
                          'accounts/login.html',
                          {'error':error,
                           'form':form})
    else:
        form = LoginForm()
    return render(request,
                      'accounts/login.html',
                      {'form':form})

def user_logout():
    pass