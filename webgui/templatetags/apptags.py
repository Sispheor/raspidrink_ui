from django import template
register = template.Library()


@register.filter
def custom_m2m(queryset, forloop_counter):
    try:
        return queryset[forloop_counter].volume
    except IndexError:
        pass