from rest_framework.routers import SimpleRouter
from django.urls import path

#Bulk-Upload-Files
from HELPERS import BulkFileUploadView, ActiveStatusChange, ArchieveStatusChange
from apps.CMS.views import (
    CheckInOutAPI,
    CheckListAPIView,
    PresentListAPIView,
    AbsentListAPIView,
    UserAttendanceListAPIView,
    DashboardAPIView,
    UserPunchHistory
)
from apps.CMS.views.Report import AttendanceAPIView

app_name = "cms"
API_URL_PREFIX = "api/"

router = SimpleRouter()

router.register("check/list",CheckListAPIView,basename="check-list")
urlpatterns = [
    path("check/",CheckInOutAPI.as_view()),
    path("check/present/", PresentListAPIView.as_view({'get': 'list'}), name="present-users"),
    path("check/absent/", AbsentListAPIView.as_view({'get': 'list'}), name="absent-users"),
    path("check/attendance/<uuid>/", UserAttendanceListAPIView.as_view({'get': 'list'}), name="attendance-users"),
    path("check/attendance/<uuid>/table-meta/", UserAttendanceListAPIView.as_view({'get': 'get_meta_for_table'}), name="attendance-users"),
    path("dashboard/", DashboardAPIView.as_view()),
     path("attendance/report/", AttendanceAPIView),
     path("punch-history/", UserPunchHistory.as_view(), name="user-punch-history"),
  
   
] + router.urls
