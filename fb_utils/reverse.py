from django import template
from django.conf import settings

import re

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