from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.ACCESS.serializers.user import RegisterSerializer, UserListReadOnlySerializer, UserWriteOnlySerializer, UserDetailSerializer
from apps.BASE.permissions import NonAuthenticatedAPIMixin
from apps.BASE.views import AppAPIView, ListAPIViewSet, CUDAPIViewSet, AbstractLookUpFieldMixin,AppCreateAPIView
from django.contrib.auth import authenticate
from apps.ACCESS.models import User
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as django_logout


# Register View
class RegisterView(AppCreateAPIView,NonAuthenticatedAPIMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

   

class LoginView(AppAPIView, NonAuthenticatedAPIMixin):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        # Authenticate user with named arguments
        user = authenticate(request, phone_number=phone_number, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "phone_number": user.phone_number,
                "token": token.key,
            }
            return self.send_response(data=data)

        return self.send_error_response(
            {"message": "Invalid phone number or password."}
        )

# Logout View
class LogoutView(AppAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user= self.get_authenticated_user()
        if user:
            Token.objects.filter(user=user).delete()
        django_logout(request)
        return self.send_response(data={"Successfully logged out"})
            
       

# class GetAuthUserDetails(AppAPIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         # Helper method to safely extract role attributes
#         def get_role_attr(attr, default=False):
#             return getattr(user.role, attr, default) if hasattr(user, "role") and user.role else default

#         return self.send_response(
#             data={
#                 "id": user.id,
#                 "identity": user.identity if hasattr(user, "identity") else None,
#                 "email": user.email if hasattr(user, "email") else None,
                
#                 "inventory_access": get_role_attr("inventory_access"),
#                 "stock_access": get_role_attr("stock_access"),
#                 "invoice_access": get_role_attr("invoice_access"),
#                 "employee_access": get_role_attr("employee_access"),
#                 "report_access": get_role_attr("report_access"),
#                 "log_access": get_role_attr("log_access"),
#             }
#         )



class UserDetailAPIView(AppAPIView):
    def get(self, request, *args, **kwargs):
        user = self.get_authenticated_user()
        
        if not user:
            return self.send_error_response({"detail": "Invalid User"})
        data = {
            "id": user.id,
            "uuid": user.uuid,
            "identity": user.identity,
            "email": user.email,
            "phone_number": user.phone_number,
        }
        return self.send_response(data)
    
    
class UserDetailEditAPIView(AppAPIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,*args,**kwargs):
        user = self.get_authenticated_user()
        identity = request.POST.get('identity')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        if identity:
            user.identity = identity
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        user.save()

        data ={
            "identity":user.identity,
            "email":user.email,
            "phone_number":user.phone_number
        }
        return self.send_response(data=data)


class UserListAppAPIView(ListAPIViewSet):
    queryset = User.objects.all()
    serializer_class= UserListReadOnlySerializer

    all_table_columns = {
        "identity":"Name",
        "phone_number":"Phone Number",
        "is_active" :"Active"
    }

    def get_meta_for_table(self):
        data = {
            "columns":self.all_table_columns,
            "filters":self.all_filters,
            "filter_data":{
                
            }
        }
        return data
    
class UserCUDAppAPIView(CUDAPIViewSet):
    queryset = User.objects.all()
    serializer_class= UserWriteOnlySerializer
    

class UserDetailsAPIView(AbstractLookUpFieldMixin, AppAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class= UserDetailSerializer




