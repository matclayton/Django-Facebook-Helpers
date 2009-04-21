"FB exceptions"


class NoFacebookUserModel(Exception):
    "FACEBOOK_USER_MODEL should read app_name.model_name in settings.py note the lack of models"
    pass

class NoFacebookUserModelinSettings(Exception):
    "FACEBOOK_USER_MODEL missing from settings.py"
    pass
