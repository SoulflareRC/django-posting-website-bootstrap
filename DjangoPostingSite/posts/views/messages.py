from posts import models
from .generics import RedirectActionView
class MessageDeleteView(RedirectActionView):
    permission_required = "delete_message"
    model = models.Message
    def actions(self):
        obj = self.get_object()
        obj.delete()