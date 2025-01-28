from apps.ACCESS.models import User
from apps.BASE.models import DEFAULT_BLANK_NULLABLE_FIELD_CONFIG, MAX_CHAR_FIELD_LENGTH, BaseModel
from django.db import models

class Check(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)
    latitude = models.FloatField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,max_length=MAX_CHAR_FIELD_LENGTH)
    longitude = models.FloatField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,max_length=MAX_CHAR_FIELD_LENGTH)
    checkin = models.CharField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,max_length=MAX_CHAR_FIELD_LENGTH)
    checkout = models.CharField(**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,max_length=MAX_CHAR_FIELD_LENGTH)


    def __str__(self):
        return self.user.identity