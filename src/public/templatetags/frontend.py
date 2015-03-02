import json
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def frontend_context(context, varname, frontend_attr):

    output = """
<script>
    window.data = window.data || {{}};
    window.data.{frontend_attr} = ko.observableArray({formatted_data});
</script>
    """
    if isinstance(varname, basestring):
        data = context[varname]
    else:
        data = varname
    data = json.dumps(data)

    return output.format(frontend_attr=frontend_attr, formatted_data=data)
