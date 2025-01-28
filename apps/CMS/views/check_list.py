from apps.BASE.views import ListAPIViewSet
from apps.CMS.models import Check
from apps.CMS.serializers import CheckInReadSerializer



class CheckListAPIView(ListAPIViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckInReadSerializer



class PresentListAPIView(ListAPIViewSet):
    serializer_class = CheckInReadSerializer

    def get_queryset(self):
        return Check.objects.filter(checkin__isnull=False)
    

class AbsentListAPIView(ListAPIViewSet):
    serializer_class = CheckInReadSerializer

    def get_queryset(self):
        return Check.objects.filter(checkin__isnull=True)
