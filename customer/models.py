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


class Country(Audit):
    class Meta:
        db_table = 'ec_country'

    country_id = models.BigAutoField(primary_key=True)

    country_name = models.CharField(max_length=255, blank=True, unique=True)
    country_code = models.CharField(max_length=255, blank=True, unique=True)


class State(Audit):
    class Meta:
        db_table = 'ec_state'

    state_id = models.BigAutoField(primary_key=True)

    state_name = models.CharField(max_length=255, blank=True, unique=True)
    state_code = models.CharField(max_length=255, blank=True, unique=True)

    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class City(Audit):
    class Meta:
        db_table = 'ec_city'

    city_id = models.BigAutoField(primary_key=True)

    city_name = models.CharField(max_length=255, blank=True, unique=True)

    state = models.ForeignKey(State, on_delete=models.CASCADE)


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

    gender = models.CharField(
        choices=GenderType.choices(), max_length=255, null=True, blank=True)

    email = models.EmailField(unique=True)

    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)

    city = models.ForeignKey(
        City, null=True, blank=True, on_delete=models.CASCADE)
    state = models.ForeignKey(
        State, null=True, blank=True, on_delete=models.CASCADE)
    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.CASCADE)
