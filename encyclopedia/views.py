from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
import markdown2 
import random
from . import util


class EntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Enter Page Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Markdown content \ne.g \n#Page Title \n\nEnter the content'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, key):
    return render(request, "encyclopedia/entrypage.html", {
        "content": util.get_entry(key.capitalize()), "title": key.capitalize()
    })

def search_view(request):
    query_dict = request.GET
    query = str(query_dict.get("q"))
    entries_list = util.list_entries()
    res_list = []
    for entry_name in entries_list:
        if query.capitalize()==entry_name:
            return render(request, "encyclopedia/entrypage.html", {
                "content": util.get_entry(query.capitalize()), "title": query.capitalize()
                })

        elif query in entry_name:
            res_list.append(entry_name)

    return render(request, "encyclopedia/searchresults.html", {"results": res_list})


def newentry_view(request):
    # print(request.POST)
    entries_list = util.list_entries()
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]
            for entry_name in entries_list:
                if entry_name == title:
                    return render(request, "encyclopedia/new_page.html", {
                        "form":form , "error": "This Entry Already Exists!!"
                    })
            
            util.save_entry(title, content)
            return render(request, "encyclopedia/entrypage.html", {
                "content": util.get_entry(title), "title": title})
                    
    context = {"form": EntryForm()}
    return render(request, "encyclopedia/new_page.html", context=context)


def editentry_view(request, key):
    entry_content = util.get_entry(key)
    form = EntryForm()
    return render(request, "encyclopedia/editpage.html", {
        "title": key, "content": entry_content
    })


def updatentry(request, key):
    entry_title = key
    entry_content = request.POST['content']
    util.save_entry(entry_title, entry_content)
    return render(request, "encyclopedia/entrypage.html", {
        "content": util.get_entry(entry_title), "title": entry_title
        })

def randomentry(request):
    entries_list = util.list_entries()
    random_index = random.randrange(len(entries_list))
    random_title = entries_list[random_index]
    return render(request, "encyclopedia/entrypage.html", {
        "content": util.get_entry(random_title), "title": random_title
        })


