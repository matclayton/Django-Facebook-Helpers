import facebook.djangofb as facebook
#from fb_utils.reverse import fbReverse
from django.conf import settings
#Attach to Specified User Model
from django.core.exceptions import ImproperlyConfigured

if not getattr(settings, 'FACEBOOK_USER_MODEL', False):
    raise NoFacebookUserModelinSettings
try:
    app_label, model_name = settings.FACEBOOK_USER_MODEL.split('.')
    User = models.get_model(app_label, model_name)
except (ImportError, ImproperlyConfigured):
    raise NoFacebookUserModel

def setup_user():
    def decorator(view):
        @facebook.require_login()
        def newview(request, *args, **kwargs):
            # Get the User object for the currently logged in user
            user = User.objects.get_current()
                    
            return view(request, user, *args, **kwargs)
        return newview
    return decorator