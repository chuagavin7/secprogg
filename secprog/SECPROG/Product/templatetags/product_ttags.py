from django import template

register = template.Library()

@register.filter(name="is_buyer")
def is_buyer(product, user):
    return product.is_buyer(user)