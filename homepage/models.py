from django.db import models

from common.models import Audit


class Categories(Audit):
    class Meta:
        db_table = 'ec_categories'

    category_id = models.AutoField(primary_key=True)
    category_title = models.CharField(max_length=255)


class Features(Audit):
    class Meta:
        db_table = 'ec_features'

    feature_id = models.AutoField(primary_key=True)

    feature_title = models.CharField(max_length=255)
    feature_keywords = models.CharField(max_length=255, null=True, blank=True)

    category_id = models.ForeignKey(
        Categories, on_delete=models.CASCADE, db_column='category_id', null=True, blank=True)

    total_sales = models.IntegerField(null=True, blank=True)

    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    max_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    min_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    arrival_date = models.DateField(null=True, blank=True)

    feature_image1 = models.FileField(
        upload_to='features/', null=True, blank=True)
    feature_image2 = models.FileField(
        upload_to='features/', null=True, blank=True)
    feature_image3 = models.FileField(
        upload_to='features/', null=True, blank=True)
    feature_image4 = models.FileField(
        upload_to='features/', null=True, blank=True)


class Banner(Audit):
    class Meta:
        db_table = 'ec_banner'

    banner_id = models.AutoField(primary_key=True)

    banner_title = models.CharField(max_length=255)
    banner_keyword = models.CharField(max_length=255, null=True, blank=True)

    banner_description = models.TextField(null=True, blank=True)

    banner_image = models.FileField(
        upload_to='banner/', null=True, blank=True)

    feature_id = models.ForeignKey(
        Features, on_delete=models.CASCADE, db_column='feature_id', null=True, blank=True)

    # promotion_id = models.ForeignKey(null=True, blank=True)
