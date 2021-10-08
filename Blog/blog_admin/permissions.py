from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin

class IsStaffOrSuperUserMixin(UserPassesTestMixin,LoginRequiredMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser