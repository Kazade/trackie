from django.db import models

from djangae import fields
from djangae.contrib.gauth.models import GaeAbstractDatastoreUser
from djangae.contrib import pagination

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(GaeAbstractDatastoreUser):
    pass


class Project(BaseModel):
    owner = models.ForeignKey(User, related_name="projects_where_owner")
    admins = fields.RelatedSetField(User, related_name="projects_where_admin", blank=True)
    members = fields.RelatedSetField(User, related_name="projects_where_member", blank=True)

    title = models.CharField(max_length=500, unique=True)

    def __unicode__(self):
        return self.title

class Object(BaseModel):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=500)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Milestone(Object):
    pass


class Severity(Object):
    pass


class Tag(Object):
    pass


@pagination.paginated_model(orderings=[ ("modified",), ("created",), ("summary",) ])
class Issue(BaseModel):
    summary = models.CharField(max_length=500)
    reporter = models.ForeignKey(User, blank=True, null=True, related_name="issues_where_reporter")
    assignee = models.ForeignKey(User, blank=True, null=True, related_name="issues_where_assignee")

    severity = models.ForeignKey(Severity)
    milestone = models.ForeignKey(Milestone)

    tags = fields.RelatedSetField(Tag)


class Update(BaseModel):
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(User)
