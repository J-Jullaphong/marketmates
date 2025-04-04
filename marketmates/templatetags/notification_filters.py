from django import template

register = template.Library()


@register.filter
def exclude(queryset, args):
    """Excludes notifications with a given field=value, usage: unread|exclude:'level=chat'"""
    try:
        field, value = args.split('=')
        return queryset.exclude(**{field.strip(): value.strip()})
    except Exception:
        return queryset
