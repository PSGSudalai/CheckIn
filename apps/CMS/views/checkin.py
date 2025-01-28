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
            return self.send_error_response({"message": "User authentication required."})

        checkin = request.data.get("checkin")
        checkout = request.data.get("checkout")
        created_at = request.data.get("created_at", now().date())
        location = request.data.get("location", {})

        latitude, longitude = location.get("latitude"), location.get("longitude")

        # Validate latitude and longitude presence
        if latitude is None or longitude is None:
            return self.send_error_response({"message": "Latitude and longitude are required."})

        try:
            latitude, longitude = float(latitude), float(longitude)
        except ValueError:
            return self.send_error_response({"message": "Invalid latitude or longitude."})

        # Check if user is within 100 meters radius
        if calculate_distance(FIXED_LATITUDE, FIXED_LONGITUDE, latitude, longitude) > MAX_DISTANCE:
            return self.send_error_response({"message": "You are out of range."})

        check, created = Check.objects.get_or_create(user=user, created_at=created_at)

        if checkin:
            if not created:
                return self.send_error_response({"message": "You have already checked in today."})

            check.checkin = checkin
            check.save()
            return self.send_response({"message": "Check-in time saved."})

        if checkout:
            if not check.checkin:
                return self.send_error_response({"message": "Cannot Check out without checking in first."})
            
            if check.checkout:
                return self.send_error_response({"message": "You have already checked out today."})

            check.checkout = checkout
            check.save()
            return self.send_response({"message": "Check-out time saved."})

        return self.send_error_response({"message": "Invalid request or conditions not met."})
