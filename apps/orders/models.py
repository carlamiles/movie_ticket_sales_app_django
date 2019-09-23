from __future__ import unicode_literals
from django.db import models
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class OrderManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name_min"] = "First name should be at least 2 characters"
        if postData['first_name'].isalpha() == False:
            errors["first_name_alpha"] = "First name must be letters only"
        if len(postData['last_name']) < 2:
            errors["last_name_min"] = "Last name should be at least 2 characters"
        if postData['last_name'].isalpha() == False:
            errors["last_name_alpha"] = "Last name must be letters only"
        if len(postData['email']) == 0:
            errors['email_missing'] = 'Please enter your email'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = "Please enter a valid email address"
        if len(postData['cc']) < 16:
            errors["credit_card_num_min"] = "Credit card number should be at least 16 digits"
        if len(postData['cc']) > 19:
            errors["credit_card_num_max"] = "Credit card number should be no more than 19 digits"
        if len(postData['exp_month']) != 2:
            errors["exp_month"] = "Credit card expiration month should be 2 digits, i.e. 10 for October or 01 for January"
        if len(postData['exp_year']) != 4:
            errors["exp_year"] = "Credit card expiration year should be 4 digits, i.e. 2019"
        if len(postData['num_tix']) == 0:
            errors["num_tix_min"] = "Number of tickets must be greater than 0"
        if len(postData['num_tix']) > 10:
            errors["num_tix_max"] = "Number of tickets per order must not be greater than 10"
        return errors

class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255)
    credit_card_num = models.BigIntegerField()
    expiry_month = models.SmallIntegerField()
    expiry_year = models.SmallIntegerField()
    sec_code = models.SmallIntegerField()
    movie_title = models.CharField(max_length=255)
    movie_date = models.CharField(max_length=255)
    movie_time = models.CharField(max_length=255)
    num_tix = models.SmallIntegerField()
    order_total = models.IntegerField()
    objects = OrderManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"<Order object: {self.first_name} {self.last_name} ({self.id}) {self.email_address} {self.credit_card_num} {self.expiry_month} {self.expiry_year} ({self.sec_code}) {self.movie_title} {self.movie_date} {self.movie_time} {self.num_tix} {self.created_at} {self.updated_at}>"