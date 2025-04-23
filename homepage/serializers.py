from rest_framework import serializers

from homepage.models import Features, Banner


class ViewFeaturesMASerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ["feature_id",
                  "feature_title",
                  "feature_keywords",
                  "feature_image1",]

        read_only_fields = fields


class ViewFeaturesWASerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ["feature_id",
                  "feature_title",
                  "feature_keywords",
                  "feature_image1",
                  "feature_image2",
                  "feature_image3",
                  "feature_image4",]
        read_only_fields = fields


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
