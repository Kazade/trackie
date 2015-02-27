from django.db import models

from djangae import fields
from djangae.contrib.gauth.models import GaeAbstractDatastoreUser
from enum import Enum

class Severity(Enum):
    VERY_LOW = Enum.Entry("VERY_LOW")
    LOW = Enum.Entry("LOW")
    MEDIUM = Enum.Entry("MEDIUM")
    HIGH = Enum.Entry("HIGH")
    CRITICAL = Enum.Entry("CRITICAL")


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(GaeAbstractDatastoreUser):
    pass


class Project(BaseModel):
    owner = models.ForeignKey(User)
    admins = fields.RelatedSetField(User)
    members = fields.RelatedSetField(User)

    title = models.CharField(max_length=500, unique=True)


class Issue(BaseModel):
    summary = models.CharField(max_length=500)
    assignee = models.ForeignKey(User, blank=True, null=True)

    severity = models.CharField(choices=Severity.choices)


class Update(BaseModel):
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(User)
