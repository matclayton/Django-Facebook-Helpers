from django import template

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