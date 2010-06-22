from django import template

register = template.Library()

#@register.inclusion_tags('_cal.html')
def cal(context):
    return {
        'test':'test',
        'user': context['user'],
    }
register.inclusion_tag('_cal.html',takes_context=True)(cal)
