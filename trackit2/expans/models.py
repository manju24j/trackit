from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
# Create your models here.
	


class Supplier(models.Model):
	user = models.OneToOneField(User)
	address = models.CharField(max_length=200)
	phoneno =models.CharField(max_length=200,unique=True)
	picture = models.ImageField(upload_to='supplier_images',default="supplier_images/img_avatar3.png")
	ratings = models.IntegerField(blank=True,default=5)

	class Meta:
		db_table="Supplier"



# DATA BASE MODEL FOR ORGANIZATION ,PROFILE TO HOLD NAME CONTACT NO AND PICTURE
class Oraganization(models.Model):
	user=models.OneToOneField(User)
	name=models.CharField(max_length=100)
	phoneno =models.CharField(max_length=10,unique=True)
	address=models.CharField(max_length=200)
	picture=models.ImageField(upload_to='org_images',default="org_images/img_avatar3.png")
	people=models.IntegerField(default=5)

	class Meta:
		db_table="Oraganization"

# DATA BASE MODEL FOR ITEMS NAME AND PIC
class Item(models.Model):
	name = models.CharField(max_length=200,unique=True)
	picture = models.ImageField(upload_to='item_pics', blank=False)

	class Meta:
	        db_table="Item"
	def __unicode__(self):
		return self.name



# DATA BASE MODEL FOR USER'S SELECTED ITEMS'
class Mylist(models.Model):
	org=models.ForeignKey(Oraganization)
	sup=models.ForeignKey(Supplier)
	item=models.ForeignKey(Item)
	measured=models.CharField(max_length=128)
	price=models.FloatField()
	payoption=models.CharField(max_length=128)
	noofusers=models.IntegerField(default=0)

	class Meta:
		db_table="Mylist"
		unique_together=(("org","item"),)



# DATA BASE MODEL FOR USER TRANSACTION
class Transaction(models.Model):
	mylist=models.ForeignKey(Mylist)
	date = models.DateTimeField(auto_now_add=True)
	qnty = models.PositiveIntegerField()
	total = models.FloatField()

	class Meta:
		db_table="Transaction"
		

class Payment(models.Model):
	mylist=models.ForeignKey(Mylist)
	date=models.DateTimeField(auto_now_add=True)
	advance=models.PositiveIntegerField(default=0)
	balance=models.FloatField(default=0)
	qnty=models.IntegerField(default=0)
	total=models.FloatField(default=0)
	due=models.FloatField(default=0)
	class Meta:
		db_table="Payment"
