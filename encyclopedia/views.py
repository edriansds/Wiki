from django.shortcuts import redirect, render
from . import util
from markdown2 import Markdown
from random import randint

# Set for pass markdown to html
md = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, content):
    """For content pages"""

    # If an entry does not exist, return an error page
    if not util.get_entry(content):
        return render(request, "encyclopedia/error.html", {
            "error": "Not Found",
        })

    # Render page
    return render(request, "encyclopedia/entry.html", {
        "title": content,
        "content": md.convert(util.get_entry(content)),
    })


def search(request):
    """Search results"""

    # Get form data
    query = request.GET.get("q").strip()
    entries = util.list_entries()
    queries = []

    for entry in entries:

        # If th questy was found in the entries
        if query.casefold() == entry.casefold():
            return redirect(f"../wiki/{entry}")

        # Matching results
        elif query.casefold() in entry.casefold():
            queries.append(entry)
            continue

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": queries,
    })


def new(request):
    """Create a new page entry"""
    if request.method == "POST":
        title = request.POST.get("title")

        # Manage exceptions:
        if title.casefold() in [entry.casefold() for entry in util.list_entries()]:
            return render(request, "encyclopedia/error.html", {
                "error": "Page already exists",
            })
        elif not title:
            return render(request, "encyclopedia/error.html", {
                "error": "Provide a title",
            })

        # Save new page
        util.save_entry(title=title, content=request.POST.get("content"))
        return redirect(f"wiki/{title}")

    return render(request, "encyclopedia/new.html")


def edit(request, entry):
    """Edit content of entry"""

    # Validate form and save data
    if request.method == "POST":
        if not request.POST.get("content"):
            return render(request, "encyclopedia/error.html", {
                "error": "missing content",
            })

        util.save_entry(entry, request.POST.get("content"))

        # Redirect to the saved page
        return redirect(f"/wiki/{entry}")

    return render(request, "encyclopedia/edit.html", {
        "content": entry,
        "edit": util.get_entry(entry),
    })


def random(request):
    """Go to a random entry"""
    # List of entries
    entries = util.list_entries()
    entry = entries[randint(0, len(entries) - 1)]

    # Render page
    return redirect(f"wiki/{entry}")

