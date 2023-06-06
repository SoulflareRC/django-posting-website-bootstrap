import datetime
from django import template
from django_comments.templatetags.comments import *
register = template.Library()
from posts import models
from django_comments.models import Comment
# simple tag can be used to return a variable directly to the context.

@register.filter
def to_class_name(value):
    return value.__class__.__name__
@register.simple_tag
def current_time(format_string=""):
    # simple tags only return plain string, nothing fancy
    return datetime.datetime.now().strftime(format_string)
@register.simple_tag
def num_range(start,end):
    # this will return a number range
    return range(start,end)
@register.simple_tag(takes_context=True)
def get_posts(context,**kwargs):
    # simple tags can also return queryset like a variable
    request = context['request']
    if request.user.is_authenticated:
        queryset = models.Post.objects.visible_to_user(request.user)
    else:
        queryset = models.Post.objects.visible_to_user(-1)
    queryset = queryset.order_by('-publish_date')
    queryset = queryset.exclude(pinned=True) # don't show pinned posts since they are already shown somewhere else.

    if 'num' in kwargs:
        return queryset[:kwargs['num']]
    return queryset
@register.simple_tag
def get_post_comments(**kwargs):
    # ordered by submit date by default
    queryset = Comment.objects.all().order_by('-submit_date')
    if 'num' in kwargs:
        return queryset[:kwargs['num']]
    if 'order' in kwargs:
        return queryset.order_by(kwargs['order'])
    return queryset

from django_comments.templatetags.comments import BaseCommentNode,CommentListNode
class CommentListAllNode(CommentListNode):
    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse get_comment_list/count/form and return a Node."""
        '''
        Usage: get_comment_list_all for app.model as comments
        '''
        tokens = token.split_contents()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for app.model as varname  %}
        elif len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                ctype=BaseCommentNode.lookup_content_type(tokens[2], tokens[0]),
                as_varname=tokens[4]
            )

        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])
    def get_queryset(self, context):

        ctype=self.ctype
        # Explicit SITE_ID takes precedence over request. This is also how
        # get_current_site operates.
        site_id = getattr(settings, "SITE_ID", None)
        if not site_id and ('request' in context):
            site_id = get_current_site(context['request']).pk

        qs = self.comment_model.objects.filter(
            content_type=ctype,
            site__pk=site_id
        ).order_by('-submit_date')



        # The is_public and is_removed fields are implementation details of the
        # built-in comment model's spam filtering system, so they might not
        # be present on a custom comment model subclass. If they exist, we
        # should filter on them.
        field_names = [f.name for f in self.comment_model._meta.fields]
        if 'is_public' in field_names:
            qs = qs.filter(is_public=True)
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(is_removed=False)
        if 'user' in field_names:
            qs = qs.select_related('user')
        # only show comments from posts visible to current user.
        if 'request' in context:
            request = context['request']
            visible_posts = models.Post.objects.visible_to_user(request.user if request.user.is_authenticated else -1)

            qs = qs.filter(object_pk__in=visible_posts)

        return qs

@register.tag
def get_comment_list_all(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_comment_list for [object] as [varname]  %}
        {% get_comment_list for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_comment_list for event as comment_list %}
        {% for comment in comment_list %}
            ...
        {% endfor %}

    """
    return CommentListAllNode.handle_token(parser, token)