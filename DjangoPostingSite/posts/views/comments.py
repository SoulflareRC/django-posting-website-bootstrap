from django_comments.views.moderation import perform_delete
from fluent_comments.models import FluentComment
from .generics import RedirectActionView
class CommentDeleteView(RedirectActionView):
    model = FluentComment
    permission_required = "fluent_comments.delete_comment"
    def actions(self):
        obj = self.get_object()
        perform_delete(self.request,obj)
        print(f"Comment {obj.comment} was deleted.")