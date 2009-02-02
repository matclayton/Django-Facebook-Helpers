from django import template
from django.conf import settings
from django.template.defaulttags import URLNode
import re

register = template.Library()

def get_version(version_attr):
  """
  Return the version number from the settings.py file or None if it is not set
  
  Example: (If settings.IMAGE_VERSION = 2)
  get_version('IMAGE_VERSION')
  
  Returns:
  2
  """
  try:
    version = getattr(settings, version_attr)
  except AttributeError:
    version = None

  return version

def version_url(url_string, version = None):
  """
  Returns a version url concatenated with the settings.MEDIA_URL
  
  Example: (If settings.MEDIA_URL = '/media/')
  
  version_url('js/jquery.js', 5)
  
  Returns:
  
  /media/js/5/jquery.js
  """
 # parts = url_string.rpartition('/')
  
  if version:
    url_string = url_string +'?v=' + str(version) 
  return settings.MEDIA_URL + url_string

@register.simple_tag
def image_url(url_string):
  """
  Returns a versioned url
  
  Example: (If settings.MEDIA_URL = '/media/' and settings.IMAGE_VERSION = 2
  {% load version_media_urls %}
  {% image_url "images/favicon.ico" %}
  
  Returns:
  
  /media/images/2/favicon.ico
  """
  return version_url('images/'+url_string, get_version('IMAGE_VERSION'))

@register.simple_tag
def css_url(url_string):
  """
  Returns a versioned url
  
  Example: (If settings.MEDIA_URL = '/media/' and settings.CSS_VERSION = 2
  {% load version_media_urls %}
  {% css_url "css/style.css" %}
  
  Returns:
  
  /media/css/2/style.css
  """
  return version_url('css/'+url_string, get_version('CSS_VERSION'))

@register.simple_tag
def fbjs_url(url_string):
  """
  Returns a versioned url
  
  Example: (If settings.MEDIA_URL = '/media/' and settings.FBJS_VERSION = 2
  {% load version_media_urls %}
  {% js_url "js/jquery.js" %}
  
  Returns:
  
  /media/js/2/jquery.js
  """
  return version_url('fbjs/'+url_string, get_version('FBJS_VERSION'))

@register.simple_tag
def swf_url(url_string):
  """
  Returns a versioned url
  
  Example: (If settings.MEDIA_URL = '/media/' and settings.FBJS_VERSION = 2
  {% load version_media_urls %}
  {% js_url "js/jquery.js" %}
  
  Returns:
  
  /media/js/2/jquery.js
  """
  return version_url('swf/'+url_string, get_version('SWF_VERSION'))


#@register.simple_tag
def fb_url(parser, token):
    """
    Returns an absolute URL matching given view with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% url path.to.some_view arg1,arg2,name1=value1 %}

    The first argument is a path to a view. It can be an absolute python path
    or just ``app_name.view_name`` without the project name if the view is
    located inside the project.  Other arguments are comma-separated values
    that will be filled in place of positional and keyword arguments in the
    URL. All arguments for the URL should be present.

    For example if you have a view ``app_name.client`` taking client's id and
    the corresponding line in a URLconf looks like this::

        ('^client/(\d+)/$', 'app_name.client')

    and this app's URLconf is included into the project's URLconf under some
    path::

        ('^clients/', include('project_name.app_name.urls'))

    then in a template you can create a link for a certain client like this::

        {% url app_name.client client.id %}

    The URL will look like ``/clients/client/123/``.
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
fb_url = register.tag(fb_url)

#@register.simple_tag
def server_url(parser, token):
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

class FBURLNode(URLNode):
    def render(self, context):
        return settings.FACEBOOK_CANVAS_URL + re.sub('^'+settings.FACEBOOK_CALLBACK_PATH,'',super(FBURLNode,self).render(context))
    
class ServerURLNode(URLNode):
    def render(self, context):
        return settings.SERVER_URL + super(ServerURLNode,self).render(context)
 