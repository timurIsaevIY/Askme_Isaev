from django import template

register = template.Library()


@register.filter()
def get_answers_count(dictionary, key):
    return dictionary.get(key)
