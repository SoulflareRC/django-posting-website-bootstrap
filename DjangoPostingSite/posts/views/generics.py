from django.views import generic
from guardian.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.shortcuts import reverse
from django.core.exceptions import PermissionDenied
class StaffRequiredMixin(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class RedirectActionView(PermissionRequiredMixin,LoginRequiredMixin,generic.RedirectView,generic.detail.SingleObjectMixin):
    '''For owner of an object to manipulate a single object, redirect upon clicking'''
    raise_exception = True
    def actions(self):
        return NotImplementedError()
    def get_fallback_url(self):
        return reverse('posts:index')
    def get_url(self):
        '''This is to get normal redirect url'''
        return None
    def get_redirect_url(self, *args, **kwargs):
        self.actions()
        if self.get_url():
            return self.get_url()
        else:
            referer = self.request.META.get('HTTP_REFERER')
            if referer:
                return referer
            else:
                return self.get_fallback_url()

