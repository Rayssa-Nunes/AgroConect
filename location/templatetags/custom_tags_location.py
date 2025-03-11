from django import template

register = template.Library()

@register.filter
def get_item(dict_list, key):
    for dictionary in dict_list:
        if key in dictionary:
            return dictionary.get(key)
    return None