# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import re
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password as _check_password
from api import errors


class Attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "attribute"


class AttributeValue(models.Model):
    attribute_value_id = models.AutoField(primary_key=True)
    attribute_id = models.IntegerField()
    value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "attribute_value"


class Audit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    created_on = models.DateTimeField()
    message = models.TextField()
    code = models.IntegerField()

    class Meta:
        managed = False
        db_table = "audit"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    department_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "category"


class CustomerManager(BaseUserManager):
    def create_customer(self, *args, **kwargs):
        email = kwargs.get("email", None)
        normalized_email = self.normalize_email(email)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", normalized_email):
            errors.handle(errors.USR_03)
        try:
            customer = self.model.objects.get(email=normalized_email)
            if customer:
                errors.handle(errors.USR_04)
        except self.model.DoesNotExist:
            kwargs.pop("email", None)
            password = kwargs.pop("password", None)
            customer = self.model(email=normalized_email, **kwargs)
            if password is not None:
                customer.set_password(password)
            customer.save()
            return customer


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(unique=True, max_length=100, default="")
    password = models.CharField(max_length=100, default="")
    credit_card = models.TextField(blank=True, null=True)
    address_1 = models.CharField(max_length=100, blank=True, null=True)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    shipping_region_id = models.IntegerField(default=1)
    day_phone = models.CharField(max_length=100, blank=True, null=True)
    eve_phone = models.CharField(max_length=100, blank=True, null=True)
    mob_phone = models.CharField(max_length=100, blank=True, null=True)

    is_active = True

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def check_password(self, raw_password):
        return _check_password(raw_password, self.password)

    class Meta:
        managed = True
        db_table = "customer"


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "department"


class OrderDetail(models.Model):
    item_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "order_detail"


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    shipped_on = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    auth_code = models.CharField(max_length=50, blank=True, null=True)
    reference    = models.CharField(max_length=50, blank=True, null=True)
    shipping_id = models.IntegerField(blank=True, null=True)
    tax_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "orders"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=150, blank=True, null=True)
    image_2 = models.CharField(max_length=150, blank=True, null=True)
    thumbnail = models.CharField(max_length=150, blank=True, null=True)
    display = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = "product"


class ProductAttribute(models.Model):
    product_id = models.IntegerField(primary_key=True)
    attribute_value_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "product_attribute"
        unique_together = (("product_id", "attribute_value_id"),)


class ProductCategory(models.Model):
    product_id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "product_category"
        unique_together = (("product_id", "category_id"),)


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    review = models.TextField()
    rating = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "review"


class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    shipping_type = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_region_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "shipping"


class ShippingRegion(models.Model):
    shipping_region_id = models.AutoField(primary_key=True)
    shipping_region = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "shipping_region"


class ShoppingCart(models.Model):
    item_id = models.AutoField(primary_key=True)
    cart_id = models.CharField(max_length=32)
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    buy_now = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "shopping_cart"


class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_type = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "tax"
