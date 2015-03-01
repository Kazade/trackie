from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView

from trackie.models import Issue, Project

from djangae.contrib.pagination import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "title"
        ]

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "summary"
        ]

class APIList(APIView):
    """An API listing that uses the djangae paginator"""

    # Just why? I hate Django's CBVs!
    queryset = None
    serializer = None
    filter_func = None

    def __init__(self, serializer, queryset, filter_func=None, *args, **kwargs):
        self._queryset = queryset
        self._serializer = serializer
        self._filter_func = filter_func

        super(APIList, self).__init__(*args, **kwargs)

    def get(self, request):
        if self._filter_func:
            queryset = self._filter_func(self._queryset, request)
        else:
            queryset = self._queryset

        paginator = Paginator(queryset, 25, readahead=10, allow_empty_first_page=True)
        page = request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            try:
                objects = paginator.page(1)
            except EmptyPage:
                objects = [] #FIXME: Djangae paginator is broken
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        serializer = self._serializer(objects, many=True)
        return Response(serializer.data)




# Why don't CBVs allow positional args??
project_list = APIList.as_view(
    serializer=ProjectSerializer,
    queryset=Project.objects.order_by("title")
)

issue_list = APIList.as_view(
    serializer=IssueSerializer,
    queryset=Issue.objects.order_by("-created"),
    filter_func=lambda qs, req: qs.filter(project=req.project)
)
