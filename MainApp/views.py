from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
            form.save()
            return redirect("snippets")
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               "snippets": snippets}
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
            "type": "view"
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

def edit_snippet(request, snippet_id):
    try:
        snippet = Snippet.objects.get(pk=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "pages/errors.html", {"error": f"Snippet with id={snippet_id} not found"})
    else:
        # if request.method == "GET":
        #     context = {
        #         "snippet": snippet,
        #         "view": "edit"
        #     }
        #     return render(request, 'pages/view_snippet.html', context)
        if request.method == "GET":
            form = SnippetForm(instance=snippet)
            return render(request, "pages/add_snippet.html", {"form": form})
        if request.method == "POST":
            data_form = request.POST
            snippet.name = data_form["name"]
            snippet.code = data_form["code"]
            snippet.save()
            return redirect("snippets")
    
        
        


def delete_snippet(request, snippet_id):
    try:
        snippet = Snippet.objects.get(pk=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "pages/errors.html", {"error": f"Snippet with id={snippet_id} not found"})
    else:
        snippet.delete()
        return redirect("snippets")
