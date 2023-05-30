from apps.dashboard_app.views import summarizing_table_graph as sv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def signin(request):
    """
    Sign in to the admin application; DEFAULT = admin password
    :param request: The request of the user
    :return: The render of the screen.
    """
    if request.user.is_authenticated:
        return sv(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')
