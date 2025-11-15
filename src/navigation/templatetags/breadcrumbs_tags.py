from django import template

register = template.Library()

@register.inclusion_tag('cotton/include/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    page = context.get('page')
    if page:
        ancestors = page.get_ancestors(inclusive=True).live().specific().exclude(depth=1)
        return {'ancestors': ancestors}
    return {'ancestors': []}