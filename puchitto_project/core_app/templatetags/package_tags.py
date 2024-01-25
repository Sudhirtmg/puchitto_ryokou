from django import template

register=template.Library()
@register.simple_tag
def cal(price,discount):
    if discount is None or discount is 0:
        return price
    cal=price
    cal=price-(price*discount/100)
    return cal
