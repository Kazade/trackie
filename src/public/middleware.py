from django.shortcuts import get_object_or_404

from trackie.models import Project

class ProjectMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        project_id = view_kwargs.get("project_id")
        if project_id:
            request.project = get_object_or_404(Project, pk=project_id)
