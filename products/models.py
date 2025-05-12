from django.db import models

from customer.models import Customer
from homepage.models import Categories
from common.models import Audit


class Products(Audit):
    class Meta:
        db_table = 'ec_products'

    product_id = models.AutoField(primary_key=True)

    product_name = models.CharField(max_length=255)
    product_keywords = models.CharField(max_length=255, null=True, blank=True)

    product_description = models.TextField(null=True, blank=True)

    product_rating = models.IntegerField(null=True, blank=True, default=0)
    product_discount = models.IntegerField(null=True, blank=True)
    product_available_quantity = models.IntegerField(null=True, blank=True)
    product_total_sales = models.IntegerField(null=True, blank=True)

    product_image = models.FileField(
        upload_to='products/', null=True, blank=True)

    product_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    product_final_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    product_arival_date = models.DateField(null=True, blank=True)

    product_category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, null=True, blank=True)

    product_brand = models.CharField(null=True, blank=True, max_length=255)

    product_dimension = models.CharField(null=True, blank=True, max_length=255)

    product_weight = models.CharField(null=True, blank=True, max_length=255)

    product_color = models.CharField(null=True, blank=True, max_length=255)

    additional_specification = models.JSONField(
        null=True, blank=True)


class ProductRatingModel(Audit):
    class Meta:
        db_table = 'ec_product_rating'

    product_rating_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_rating = models.TextField(null=True, blank=True)
    product_review = models.TextField(null=True, blank=True)


class ProductReviewModel(Audit):
    class Meta:
        db_table = 'ec_product_review'

    product_review_id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_review = models.TextField(null=True, blank=True)
