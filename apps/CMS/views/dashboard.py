from apps.ACCESS.models import User
from apps.BASE.views import AppAPIView
from apps.CMS.models import Check
from django.utils.timezone import now

class DashboardAPIView(AppAPIView):
    def get(self,request):
        current_today = now().date()
        employee_count = User.objects.all().count()
        present_count = Check.objects.filter(created_at=current_today).count()
        absent_count = employee_count - present_count

        data={
            "employee_count":employee_count,
            "present_count":present_count,
            "absent_count":absent_count
        }

        return self.send_response(data)
    