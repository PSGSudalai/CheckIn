from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
from django.utils.timezone import now

from apps.BASE.views import AppAPIView
from apps.CMS.models import Check

FIXED_LATITUDE = 8.5103250
FIXED_LONGITUDE = 77.5601929
MAX_DISTANCE = 100  # meters

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    
    # Haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371000 * 2 * atan2(sqrt(a), sqrt(1 - a))  # Result in meters

class CheckInOutAPI(AppAPIView):
    def post(self, request):
        user = self.get_authenticated_user()
        if not user:
            return self.send_error_response(
                {"message": "User authentication required."}
            )

        punch_in, punch_out, punch_date = (
            request.data.get("punch_in"),
            request.data.get("punch_out"),
            request.data.get("punch_date"),
        )
        location = request.data.get("location", {})
        latitude, longitude = location.get("latitude"), location.get("longitude")

        if latitude is None or longitude is None:
            return self.send_error_response(
                {"message": "Latitude and longitude are required."}
            )

        try:
            latitude, longitude = float(latitude), float(longitude)
        except ValueError:
            return self.send_error_response(
                {"message": "Invalid latitude or longitude."}
            )

        if (
            calculate_distance(FIXED_LATITUDE, FIXED_LONGITUDE, latitude, longitude)
            > MAX_DISTANCE
        ):
            return self.send_error_response({"message": "You are out of range."})

        punch = Check.objects.filter(user=user, punch_date=punch_date).first()

        if punch_in:
            if punch:
                return self.send_error_response(
                    {"message": "You have already punched in today."}
                )
            Check.objects.create(user=user, punch_in=punch_in, punch_date=punch_date)
            return self.send_response({"message": "Punch in time saved."})

        if punch_out:
            if not punch or not punch.punch_in:
                return self.send_error_response(
                    {"message": "Cannot punch out without punching in first."}
                )
            if punch.punch_out:
                return self.send_error_response(
                    {"message": "You have already punched out today."}
                )
            punch.punch_out = punch_out
            punch.save()
            return self.send_response({"message": "Punch out time saved."})

        return self.send_error_response({"message": "Invalid request or conditions not met."})
    



class UserPunchHistory(AppAPIView):
    def get(self, request):
        user = self.get_authenticated_user()
        if not user:
            return self.send_error_response(
                {"message": "User authentication required."}
            )

        punches = Check.objects.filter(user=user).order_by("punch_date")
        punch_data = [
            {
                "punch_date": punch.punch_date,
                "punch_in": punch.punch_in,
                "punch_out": punch.punch_out,
            }
            for punch in punches
        ]
        return self.send_response({"punch_data": punch_data})