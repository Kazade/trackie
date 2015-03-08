from django.shortcuts import render, redirect
from public.forms import IssueForm

from api.views import issue_list, project_list

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

def landing(request):
    subs = {}
    subs["projects"] = project_list(request).data
    return render(request, "public/landing.html", subs)

def project_home(request, project_id):
    subs = {}
    subs["issues"] = issue_list(request).data
    subs["nav"] = _generate_nav(request)
    return render(request, "public/project_home.html", subs)

def project_issue(request, project_id, issue_id):
    subs = {}
    subs["nav"] = _generate_nav(request)
    return render(request, "public/project_issue.html", subs)

def project_new_issue(request, project_id):
    subs = {}

    if request.method == "POST":
        form = IssueForm(request.project, request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect("project_issue", project_id=project_id, issue_id=instance.pk)
    else:
        form = IssueForm(request.project)

    subs["form"] = form
    return render(request, "public/project_new_issue.html", subs)
