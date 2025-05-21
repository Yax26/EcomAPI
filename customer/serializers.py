from rest_framework import serializers

from customer.models import City, Country, Customer, State


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "middle_name",
                  "last_name", "password", "email"]


class EditPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "middle_name",
                  "last_name", "gender", "age", "contact_number", "department"]


class FetchPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "middle_name",
                  "last_name", "email", "gender", "age", "contact_number", "department"]

        read_only_fields = fields


class EditAddressInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["city", "state",
                  "country", "postal_code", "street"]


class FetchAddressInfoSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ["city", "state",
                  "country", "postal_code", "street"]
        read_only_fields = fields

    def get_country(self, obj):
        if obj.country and obj.country.country_name:
            return obj.country.country_name
        return None

    def get_state(self, obj):
        if obj.state and obj.state.state_name:
            return obj.state.state_name
        return None

    def get_city(self, obj):
        if obj.city and obj.city.city_name:
            return obj.city.city_name
        return None


class AddCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class FetchCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["country_id", "country_name", "country_code"]
        read_only_fields = fields


class AddStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class FetchStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["state_id", "state_name", "state_code", "country"]
        read_only_fields = fields


class AddCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class FetchCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["city_id", "city_name", "state"]
        read_only_fields = fields
