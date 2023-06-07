from django.http import HttpRequest
from . import models
def site_settings(request:HttpRequest):
    print("What!!!!")
    site_setting = models.SiteInfo.objects.first()
    print("Site setting:",site_setting)

    return {"site_setting": site_setting}
