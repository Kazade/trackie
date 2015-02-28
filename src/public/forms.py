from django import forms
from trackie.models import Issue, Project


class BootstrapMixin(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        for name, field in self.fields.iteritems():
            field.widget.attrs["class"] = "form-control"

class IssueForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Issue
        fields = [ "summary", "tags" ]

    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, project, *args, **kwargs):
        assert isinstance(project, Project)
        self.project = project

        super(IssueForm, self).__init__(*args, **kwargs)
