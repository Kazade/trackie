from django.contrib import admin

from trackie.models import (
    Project,
    Issue,
    Update,
    User
)

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Update)
admin.site.register(User)
