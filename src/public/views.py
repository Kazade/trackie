from django.shortcuts import render, redirect
from djangae.contrib.pagination import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from trackie.models import Issue
from public.forms import IssueForm

def _generate_nav(request):
    items = [
        [

        ],
        [
            { "type": "search", "text": "Search" },
        ]
    ]

    for item in items[0] + items[1]:
        if item["type"] == "link" and item["url"] == request.path:
            item["active"] = True

    return items

def project_home(request, project_id):
    subs = {}

    issues = Issue.objects.order_by("-created")
    paginator = Paginator(issues, 25, readahead=10, allow_empty_first_page=True) # Show 25 testusers per page, readahead 10 pages

    page = request.GET.get('page')
    try:
        # Under the hood this will instead order and filter by the magically generated field for
        # first_name, allowing you to efficiently jump to a specific page
        issues = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        try:
            issues = paginator.page(1)
        except EmptyPage:
            issues = [] #FIXME: Djangae paginator is broken
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        issues = paginator.page(paginator.num_pages)

    subs["issues"] = issues
    subs["nav"] = _generate_nav(request)
    return render(request, "public/project_home.html", subs)

def project_issue(request, project_id, issue_id):
    subs = {}
    subs["nav"] = _generate_nav(request)
    return render(request, "public/project_issue.html", subs)

def project_new_issue(request, project_id):
    subs = {}

    if request.method == "post":
        form = IssueForm(request.project, request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect("project_issue", project_id=project_id, issue_id=instance.pk)
    else:
        form = IssueForm(request.project)

    subs["form"] = form
    return render(request, "public/project_new_issue.html", subs)
