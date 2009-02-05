from django import template
from django.conf import settings
from django.template import Node
from fb_utils.reverse import fbReverse
from fb_utils.templatetags import *
from django.core.urlresolvers import reverse

register = template.Library()

class FBURLNode(Node):
    def __init__(self, view_name, args, kwargs):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        from django.core.urlresolvers import NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        try:
            return fbReverse(self.view_name, args=args, kwargs=kwargs)
        except NoReverseMatch:
            try:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                return fbReverse(project_name + '.' + self.view_name,
                                   args=args, kwargs=kwargs)
            except NoReverseMatch:
                return ''

def fb_url(parser, token):
    """
    Just like Django's url tag, except also works inside Facebook.
    """
    bits = token.contents.split(' ', 2)
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    args = []
    kwargs = {}
    if len(bits) > 2:
        for arg in bits[2].split(','):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                kwargs[k] = parser.compile_filter(v)
            else:
                args.append(parser.compile_filter(arg))
    return FBURLNode(bits[1], args, kwargs)
fbUrl = register.tag(fb_url)

class ServerURLNode(Node):
    def __init__(self, view_name, args, kwargs):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        from django.core.urlresolvers import NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        try:
            return '%s%s' % (settings.SERVER_BASE , reverse(self.view_name, args=args, kwargs=kwargs))
        except NoReverseMatch:
            try:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                return reverse(project_name + '.' + self.view_name,
                                   args=args, kwargs=kwargs)
            except NoReverseMatch:
                return ''

def server_url(parser, token):
    """
    Just like Django's url tag, except also works inside Facebook.
    """
    bits = token.contents.split(' ', 2)
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    args = []
    kwargs = {}
    if len(bits) > 2:
        for arg in bits[2].split(','):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                kwargs[k] = parser.compile_filter(v)
            else:
                args.append(parser.compile_filter(arg))
    return ServerURLNode(bits[1], args, kwargs)
server_url = register.tag(server_url)

 