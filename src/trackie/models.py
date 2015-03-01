from django.db import models

from djangae import fields
from djangae.contrib.gauth.models import GaeAbstractDatastoreUser
from djangae.contrib import pagination
from djangae.db import transaction

def allocate_new_id(model_class):
    from google.appengine.api import datastore
    from google.appengine.ext import db

    key = datastore.Key.from_path(model_class._meta.db_table, 1)
    ids = db.allocate_ids(key, 1)
    return range(ids[0], ids[1] + 1)[0]

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(GaeAbstractDatastoreUser):
    pass


@pagination.paginated_model(orderings=[ ("modified",), ("created",), ("title",) ])
class Project(BaseModel):
    owner = models.ForeignKey(User, related_name="projects_where_owner")
    admins = fields.RelatedSetField(User, related_name="projects_where_admin", blank=True)
    members = fields.RelatedSetField(User, related_name="projects_where_member", blank=True)

    title = models.CharField(max_length=500, unique=True)

    default_severity = models.ForeignKey("trackie.Severity", related_name="projects_where_default", blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If we are adding, we need to create the default objects
        if not self.default_severity_id:
            self.default_severity_id = allocate_new_id(Severity)
            with transaction.atomic(xg=True):
                super(Project, self).save(*args, **kwargs)
                Severity.objects.get_or_create(id=self.default_severity_id, defaults=dict(project=self, name="Normal", is_default=True))
        else:
            super(Project, self).save(*args, **kwargs)


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
    is_default = models.BooleanField(default=False)


class Tag(Object):
    pass


@pagination.paginated_model(orderings=[ ("modified",), ("created",), ("summary",) ])
class Issue(BaseModel):
    project = models.ForeignKey(Project)

    summary = models.CharField(max_length=500)
    reporter = models.ForeignKey(User, blank=True, null=True, related_name="issues_where_reporter")
    assignee = models.ForeignKey(User, blank=True, null=True, related_name="issues_where_assignee")

    severity = models.ForeignKey(Severity)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)

    tags = fields.RelatedSetField(Tag, blank=True)

    votes = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.severity_id:
            self.severity = self.project.default_severity
        super(Issue, self).save(*args, **kwargs)


class Update(BaseModel):
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(User)
