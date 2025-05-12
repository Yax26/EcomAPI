from django.db import models

from customer.models import Customer
from common.models import Audit


class Cart(Audit):
    class Meta:
        db_table = "ec_cart"
    cart_id = models.AutoField(primary_key=True)
    products = models.JSONField(null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_fees = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    is_checked_out = models.BooleanField(default=False)
