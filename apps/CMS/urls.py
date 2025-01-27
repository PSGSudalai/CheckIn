from rest_framework.routers import SimpleRouter
from django.urls import path

#Bulk-Upload-Files
from HELPERS import BulkFileUploadView, ActiveStatusChange, ArchieveStatusChange

app_name = "cms"
API_URL_PREFIX = "api/"

router = SimpleRouter()


urlpatterns = [
   
] + router.urls
