from django.http import HttpRequest
from . import models
def site_settings(request:HttpRequest):
    # print("What!!!!")
    site_setting = models.SiteInfo.objects.first()
    # print("Site setting:",site_setting)

    return {"site_setting": site_setting}
def messages(request:HttpRequest):
    user = request.user
    if not user.is_authenticated:
        return { }
    else:
        unread_msgs = models.Message.objects.filter(to_user=user,read=False)
        return {
            "unread_msgs":unread_msgs
        }