try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
    
from django.core.cache import cache
from django.utils.encoding import iri_to_uri

def fb_cache_control(**kwargs):

    def _cache_controller(viewfunc):

        def _cache_controlled(request, *args, **kw):
            cache_key = 'fbml_cache_%s_%s' % (iri_to_uri(request.path), request.facebook.uid)
            response = cache.get(cache_key)
            if not response:
                print('not_found')
                response = viewfunc(request, *args, **kw)
                cache.set(cache_key, response, 21600) #Cache for 6 hours
            return response

        return wraps(viewfunc)(_cache_controlled)

    return _cache_controller