from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required(login_url='index')
def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets")
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {'pagename': 'Просмотр сниппетов',
               "snippets": snippets,
               "count": snippets.count()}
    return render(request, 'pages/view_snippets.html', context)


def snippet_page(request, snippet_id):
    try:
        snippet = Snippet.objects.get(pk=snippet_id)
    except ObjectDoesNotExist:  
        return render(request, "pages/errors.html", {"error": f"Snippet with id={snippet_id} not found"})
    else:
        context = {
            "pagename": "Просмотр сниппета",
            "snippet": snippet,
            "type": "view",
            "comments_form": CommentForm()
        }
        return render(request, "pages/view_snippet.html", context)


# def create_snippet(request):
#    if request.method == "POST":
#        form = SnippetForm(request.POST)
#        #from pprint import pprint
#        #pprint(form)
#        if form.is_valid():
#            form.save()
#            return redirect("snippets")
#        return render(request,'page/add_snippet.html', {'form': form})

@login_required
def edit_snippet(request, snippet_id):
    try:
        snippet = Snippet.objects.filter(user=request.user).get(pk=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "pages/errors.html", {"error": f"Snippet with id={snippet_id} not found"})
    else:
        if request.method == "GET":
            context = {
                "snippet": snippet,
                "view": "edit"
            }
            return render(request, 'pages/view_snippet.html', context)
        # if request.method == "GET":
        #     form = SnippetForm(instance=snippet)
        #     return render(request, "pages/add_snippet.html", {"form": form})
        if request.method == "POST":
            data_form = request.POST
            snippet.name = data_form["name"]
            snippet.code = data_form["code"]
            snippet.public = data_form.get("public", False)
            snippet.save()
            return redirect("snippets")
    

@login_required
def delete_snippet(request, snippet_id):
    try:
        snippet = Snippet.objects.get(pk=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "pages/errors.html", {"error": f"Snippet with id={snippet_id} not found"})
    else:
        snippet.delete()
        return redirect("snippets")
    

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["wrong username or password"]
            }  
            return render(request, "pages/index.html", context)
    return redirect("index")


def logout(request):
    auth.logout(request)
    return redirect("index")

@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
            "snippets": snippets,
            "pagename": "Просмотр моих сниппетов"
        }
    return render(request, "pages/view_snippets.html", context)


def user_register(request):
    context = {'pagename': 'Добавление нового пользователя'}
    if request.method == "GET":
        form = UserRegistrationForm()
        context['form']= form
        return render(request, 'pages/registration.html', context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            context['form']= form
            return redirect("index")
        return render(request, 'pages/registration.html', context)
    
@login_required
def add_comment(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect(f'/snippet/{snippet_id}')
    raise Http404
