from rest_framework.routers import SimpleRouter
from django.urls import path

#Bulk-Upload-Files
from HELPERS import BulkFileUploadView, ActiveStatusChange, ArchieveStatusChange
from apps.CMS.views import CheckInOutAPI,CheckListAPIView,PresentListAPIView,AbsentListAPIView

app_name = "cms"
API_URL_PREFIX = "api/"

router = SimpleRouter()

router.register("check/list",CheckListAPIView,basename="check-list")
urlpatterns = [
    path("check/in/",CheckInOutAPI.as_view()),
    path("check/present/", PresentListAPIView.as_view({'get': 'list'}), name="present-users"),
    path("check/absent/", AbsentListAPIView.as_view({'get': 'list'}), name="absent-users"),
   
] + router.urls
