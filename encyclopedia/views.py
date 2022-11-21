from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from markdown2 import Markdown
import random


def index(request):

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry_page(request, title):

    # If click edit button
    if request.POST.get("save"):
        content = request.POST.get("content")
        util.save_entry(title, content)

    # is to {title} page , and not found
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", status=404)

    # If found that page , access to that entry_page by GET
    markdown = Markdown()
    html = markdown.convert(text=util.get_entry(title))

    return render(
        request,
        "encyclopedia/entry_page.html",
        context={"entry_name": title, "content": html},
    )


def search(request):
    query = request.GET.get("q", "")
    content = util.get_entry(query)

    # 如果搜尋沒有吻合的頁面 檢查sub string
    if not content:
        temp = []
        entries = util.list_entries()
        for entry in entries:
            if query.lower() in entry.lower():
                temp.append(entry)

        return render(request, "encyclopedia/search.html", {"entries": temp})

    return HttpResponseRedirect(f"wiki/{query}")


def create(request):

    if request.method == "POST":
        title = request.POST.get("title")
        context = request.POST.get("context")

        # if input valid ,return input error
        if not (title or context):
            pass

        # if new page not exist, save it and redirect
        if not util.get_entry(title):
            util.save_entry(title, context)

        # exist, then just redirect
        return HttpResponseRedirect(f"/wiki/{title}")

    return render(request, "encyclopedia/create_page.html")


def edit(request, title):
    # to get original content in that topic
    markdown = Markdown()
    html = markdown.convert(text=util.get_entry(title))

    # if is search
    if request.POST.get("edit"):
        return render(
            request, "encyclopedia/edit.html", {"entry_name": title, "content": html}
        )


# Get entrys' name list, random one and redirect
def random_page(request):
    title = random.choice(util.list_entries())
    #參數一要指向 url 的名字
    return redirect("entry", title=title)
