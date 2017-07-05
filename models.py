from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

# Create your models here.
class Person(models.Model):
	user = models.CharField(max_length=20, unique=True)
	# pwd = models.CharField(max_length=20)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	age = models.IntegerField()
	email_id = models.EmailField(unique=True)
	dob = models.DateField()
	date_created = models.DateTimeField(auto_now=True)
	phone = models.CharField(max_length=10, unique=True)
	address = models.CharField(max_length=200)

	def __unicode__(self):
		return unicode(self.user)


class DealersInfo(models.Model):
	person_info = models.OneToOneField(Person) 
	company_name = models.CharField(max_length=50)
	dl1 = models.CharField(max_length=15, unique=True)
	dl2 = models.CharField(max_length=15, unique=True)
	tin = models.CharField(max_length=15, unique=True)

	def __unicode__(self):
		return unicode(self.person_info.first_name + self.person_info.last_name)


class ComplteStockDetails(models.Model):
    batch_num = models.IntegerField(unique=True)
    item_name = models.CharField(max_length=50, unique=True)
    company = models.CharField(max_length=30)
    price_per_unit = models.FloatField()
    manf_date = models.DateField()
    exp_date = models.DateField()
    quantity = models.IntegerField()
    dealer = models.ForeignKey(DealersInfo)
    comments = models.CharField(max_length=100)
    margin = models.CharField(max_length=20)
    vat = models.CharField(max_length=20)


    def __unicode__(self):
        return unicode(self.item_name)

class Billings(models.Model):
	bill_number = models.AutoField(primary_key=True)
	bill_items = JSONField()
	bill_date = models.DateTimeField(auto_now_add=True)
	bill_user = models.ForeignKey(Person)
	bill_amount = models.DecimalField(max_digits=10, decimal_places=4)

	def __unicode__(self):
		return str(self.bill_number)