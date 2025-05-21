from enum import Enum
from django.db import models

from common.models import Audit


class GenderType(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"

    @classmethod
    def choices(cls):
        return [(type.name, type.value) for type in cls]


class Customer(Audit):
    class Meta:
        db_table = 'ec_customer'

    customer_id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=255,)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    age = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)

    gender = models.CharField(
        choices=GenderType.choices(), max_length=255, null=True, blank=True)

    email = models.EmailField(unique=True)

    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
