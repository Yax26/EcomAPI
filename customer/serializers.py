from rest_framework import serializers

from customer.models import Customer


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "middle_name",
                  "last_name", "password", "email"]


class FetchProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "middle_name",
                  "last_name", "email", "gender", "age", "contact_number", "department", "city", "state",
                  "country", "postal_code", "street"]

        read_only_fields = fields


class EditDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["department"]


class EditPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "middle_name",
                  "last_name", "gender", "age", "contact_number"]


class EditAddressInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["city", "state",
                  "country", "postal_code", "street"]
