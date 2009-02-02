from django import template
from django.conf import settings
from django.template import Node

import re

register = template.Library()

def fbReverse(view, args=None, kwargs=None):
    '''
    Much like django.core.urlresolvers.reverse, except works
    in Facebook. Returns an absolute URL to a Facebook canvas
    page.
    '''
    from django.core.urlresolvers import reverse
    ret = reverse(view, args=args, kwargs=kwargs)
    app_url = re.sub('^'+settings.FACEBOOK_CALLBACK_PATH,'',ret)
    ret_url = 'http://apps.facebook.com/%s/%s' % (settings.FACEBOOK_APP_NAME, app_url)
    return ret_url

class FBURLNode(Node):
    def __init__(self, view_name, args, kwargs):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):

        reverseFunc = fbReverse

        from django.core.urlresolvers import NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        try:
            return reverseFunc(self.view_name, args=args, kwargs=kwargs)
        except NoReverseMatch:
            try:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                return reverseFunc(project_name + '.' + self.view_name,
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

 