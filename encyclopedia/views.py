import markdown2
import random
from django.shortcuts import render
from django.contrib import messages
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html")
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(util.get_entry(title)),
    })


def search(request):
    name = request.GET.get("q", "")
    entries = util.list_entries()
    listsubs = []
    listcontents = []
    if name in entries:
        return render(request, "encyclopedia/entry.html", {
            "title": name,
            "content": markdown2.markdown(util.get_entry(name)),
        })
    
    for entry in entries:
        if name.lower() in entry.lower():
            listsubs.append(entry)
            listcontents.append(util.get_entry(entry))
            
    return render(request, "encyclopedia/search.html",{
        "listsubs": listsubs,
        "listcontents": listcontents,
    })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        listentries = util.list_entries()

        if title in listentries:
            messages.error(request, "There is already an entry with this title. Please choose another one.")
            return render(request, "encyclopedia/new.html",{
                "title": title,
                "content": content,
            })
        
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdown2.markdown(content),
        })

    return render(request,"encyclopedia/new.html")

def randompage(request):
    number = len(util.list_entries())
    guess = random.randint(0, number-1)
    guess_title = util.list_entries()[guess]
    guess_content = util.get_entry(guess_title)
    return render(request, "encyclopedia/entry.html",{
        "title": guess_title,
        "content": markdown2.markdown(guess_content),
    })

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content),
        })


    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
    })
