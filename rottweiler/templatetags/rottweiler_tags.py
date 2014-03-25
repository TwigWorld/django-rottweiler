from django import template

from rulez.templatetags.rulez_perms import rulez_perms

register = template.Library()


class RottweilerPermsNode(template.Node):
    def __init__(self, codename, varname):
        self.codename = codename
        self.varname = varname

    def render(self, context):
        user_obj = template.resolve_variable('user', context)
        context[self.varname] = user_obj.has_perm(self.codename)
        return ''


def rottweiler_perms(parser, token):
    """
    Template tag to check for global permissions or permissions
    against a particular instance.

    Usage:
        {% load rottweiler_tags %}

        {% rottweiler_perms can_edit an_instance as boolean_varname %}
        {% if boolean_varname %}
            You have permissions on this instance
        {% else %}
            You do not have permissions on this instance
        {% endif %}

        {% rottweiler_perms can_edit as boolean_varname %}
        {% if boolean_varname %}
            You have global permissions
        {% else %}
            You do not have global permissions
        {% endif %}
    """
    bits = token.split_contents()
    if len(bits) == 5:
        return rulez_perms(parser, token)
    if len(bits) != 4:
        raise template.TemplateSyntaxError(
            'tag requires two or three arguments')
    if bits[2] != 'as':
        raise template.TemplateSyntaxError(
            "second argument to tag must be 'as'")
    return RottweilerPermsNode(bits[1], bits[3])

register.tag(rottweiler_perms)
